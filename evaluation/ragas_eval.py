import json
import re
import sys
import types
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.app_settings import AppSettingsService
from services.rag_service import RAGService


DEFAULT_BENCHMARK_PATH = Path(__file__).with_name("benchmark.json")


@dataclass
class BenchmarkCase:
    question: str
    expected_answer: str
    expected_sources: list[str]


@dataclass
class EvaluationRow:
    question: str
    expected_answer: str
    generated_answer: str
    expected_sources: list[str]
    retrieved_sources: list[str]
    answer_correctness: float
    context_alignment: float
    overall_quality: float
    response_time_ms: int | None
    metric_backend: str


class RAGEvaluator:
    def __init__(self, benchmark_path: str | Path = DEFAULT_BENCHMARK_PATH):
        self.benchmark_path = Path(benchmark_path)
        self.cases = self._load_cases()

    def _load_cases(self) -> list[BenchmarkCase]:
        if not self.benchmark_path.exists():
            raise FileNotFoundError(f"Benchmark file not found: {self.benchmark_path}")

        payload = json.loads(self.benchmark_path.read_text(encoding="utf-8"))
        cases = []
        for item in payload:
            cases.append(
                BenchmarkCase(
                    question=item["question"],
                    expected_answer=item["expected_answer"],
                    expected_sources=item.get("expected_sources", []),
                )
            )
        return cases

    def run(self, settings: dict[str, Any] | None = None) -> dict[str, Any]:
        active_settings = settings or AppSettingsService().load_settings()
        rag = RAGService(settings=active_settings)

        rows: list[EvaluationRow] = []
        for case in self.cases:
            rows.append(self._evaluate_case(rag, case))

        summary = self._summarize(rows)
        return {
            "summary": summary,
            "rows": [asdict(row) for row in rows],
        }

    def _evaluate_case(self, rag: RAGService, case: BenchmarkCase) -> EvaluationRow:
        import time

        start = time.perf_counter()
        result = rag.ask(case.question)
        elapsed_ms = int((time.perf_counter() - start) * 1000)

        generated_answer = result.get("answer", "") if isinstance(result, dict) else str(result)
        sources = result.get("sources", []) if isinstance(result, dict) else []
        retrieved_sources = [f"{source['document_name']}#page-{source['page']}" for source in sources]

        ragas_metrics = self._try_ragas_metrics(case, generated_answer, sources)
        if ragas_metrics is not None:
            answer_correctness, context_alignment, overall_quality, backend_name = ragas_metrics
        else:
            answer_correctness = self._answer_correctness(case.expected_answer, generated_answer)
            context_alignment = self._context_alignment(case.expected_answer, sources)
            overall_quality = round((answer_correctness + context_alignment) / 2, 4)
            backend_name = "local_fallback"

        return EvaluationRow(
            question=case.question,
            expected_answer=case.expected_answer,
            generated_answer=generated_answer,
            expected_sources=case.expected_sources,
            retrieved_sources=retrieved_sources,
            answer_correctness=answer_correctness,
            context_alignment=context_alignment,
            overall_quality=overall_quality,
            response_time_ms=elapsed_ms,
            metric_backend=backend_name,
        )

    def _try_ragas_metrics(self, case: BenchmarkCase, generated_answer: str, sources: list[dict[str, Any]]):
        self._install_ragas_compat_shims()

        try:
            from datasets import Dataset
            from langchain_huggingface import HuggingFaceEmbeddings
            from langchain_groq import ChatGroq
            from ragas import evaluate
            from ragas.metrics import answer_correctness, answer_relevancy, faithfulness, context_precision
        except Exception:
            return None

        try:
            settings = AppSettingsService().load_settings()
            embeddings = HuggingFaceEmbeddings(model_name=settings["models"]["embedding_model"])
            llm = ChatGroq(model=settings["models"]["llm_model"])

            contexts = [source.get("chunk_preview", "") for source in sources]
            dataset = Dataset.from_dict(
                {
                    "question": [case.question],
                    "answer": [generated_answer],
                    "ground_truth": [case.expected_answer],
                    "contexts": [contexts],
                }
            )
            result = evaluate(
                dataset,
                metrics=[answer_correctness, answer_relevancy, faithfulness, context_precision],
                llm=llm,
                embeddings=embeddings,
            )
            def _get_mean(metric_name):
                values = result[metric_name]
                if hasattr(values, "mean"):
                    return float(values.mean())
                return float(sum(values) / len(values)) if values else 0.0

            answer_correctness_score = _get_mean("answer_correctness")
            context_alignment_score = float(
                (
                    _get_mean("faithfulness")
                    + _get_mean("context_precision")
                    + _get_mean("answer_relevancy")
                ) / 3
            )
            overall_quality = round((answer_correctness_score + context_alignment_score) / 2, 4)
            return (
                round(answer_correctness_score, 4),
                round(context_alignment_score, 4),
                overall_quality,
                "ragas",
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            return None

    @staticmethod
    def _install_ragas_compat_shims():
        package_names = [
            "langchain_community.chat_models",
            "langchain_community.chat_models.vertexai",
        ]

        for name in package_names:
            if name not in sys.modules:
                sys.modules[name] = types.ModuleType(name)

        vertexai_module = sys.modules["langchain_community.chat_models.vertexai"]

        class ChatVertexAI:  # pragma: no cover - compatibility shim only
            def __init__(self, *args, **kwargs):
                raise RuntimeError("ChatVertexAI is not available in this environment")

        vertexai_module.ChatVertexAI = ChatVertexAI
        sys.modules["langchain_community.chat_models"].vertexai = vertexai_module

    def _summarize(self, rows: list[EvaluationRow]) -> dict[str, Any]:
        if not rows:
            return {
                "case_count": 0,
                "average_answer_correctness": 0.0,
                "average_context_alignment": 0.0,
                "average_overall_quality": 0.0,
                "average_response_time_ms": 0.0,
                "metric_backend": "local_fallback",
            }

        return {
            "case_count": len(rows),
            "average_answer_correctness": round(sum(r.answer_correctness for r in rows) / len(rows), 4),
            "average_context_alignment": round(sum(r.context_alignment for r in rows) / len(rows), 4),
            "average_overall_quality": round(sum(r.overall_quality for r in rows) / len(rows), 4),
            "average_response_time_ms": round(sum((r.response_time_ms or 0) for r in rows) / len(rows), 2),
            "metric_backend": rows[0].metric_backend,
        }

    @staticmethod
    def _normalize_text(text: str) -> str:
        return re.sub(r"\s+", " ", text.strip().lower())

    @staticmethod
    def _answer_correctness(expected: str, actual: str) -> float:
        expected_tokens = {token for token in re.findall(r"[a-z0-9]+", expected.lower()) if len(token) > 2}
        actual_tokens = {token for token in re.findall(r"[a-z0-9]+", actual.lower()) if len(token) > 2}
        if not expected_tokens:
            return 0.0
        exact_match = float(RAGEvaluator._normalize_text(expected) == RAGEvaluator._normalize_text(actual))
        token_overlap = len(expected_tokens & actual_tokens) / len(expected_tokens)
        return round((exact_match + token_overlap) / 2, 4)

    @staticmethod
    def _context_alignment(expected_answer: str, sources: list[dict[str, Any]]) -> float:
        if not sources:
            return 0.0

        expected_tokens = {token for token in re.findall(r"[a-z0-9]+", expected_answer.lower()) if len(token) > 2}
        if not expected_tokens:
            return 0.0

        context_text = " ".join(source.get("chunk_preview", "") for source in sources).lower()
        context_tokens = {token for token in re.findall(r"[a-z0-9]+", context_text) if len(token) > 2}
        return round(len(expected_tokens & context_tokens) / len(expected_tokens), 4)


def load_benchmark_cases(path: str | Path = DEFAULT_BENCHMARK_PATH) -> list[dict[str, Any]]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def run_evaluation(
    benchmark_path: str | Path = DEFAULT_BENCHMARK_PATH,
    settings: dict[str, Any] | None = None,
) -> dict[str, Any]:
    evaluator = RAGEvaluator(benchmark_path=benchmark_path)
    return evaluator.run(settings=settings)


if __name__ == "__main__":
    print(json.dumps(run_evaluation(), indent=2))
