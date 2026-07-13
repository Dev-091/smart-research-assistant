from llm.llm_client import LLMClient
from llm.prompt_builder import PromptBuilder


class RAGPipeline:
    def __init__(self, retriever, llm_settings=None):
        self.retriever = retriever
        self.prompt_builder = PromptBuilder()
        self.llm = LLMClient(**(llm_settings or {}))

    def ask(self, query):
        query_embedding = self.retriever.embedding_model.embed_query(query)
        scored_documents = self.retriever.vector_store.similarity_search_with_scores(
            query_embedding,
            self.retriever.top_k,
        )
        documents = [doc for doc, _ in scored_documents]
        scores = [score for _, score in scored_documents]
        prompt = self.prompt_builder.build_prompt(query, documents)
        answer = self.llm.generate(prompt)
        citations = self.prompt_builder.build_citation_metadata(documents, scores=scores)

        return {
            "answer": answer,
            "sources": citations,
        }
