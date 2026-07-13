from config import FAISS_STORAGE_PATH

from embeddings.embedding_model import EmbeddingModel
from rag.pipeline import RAGPipeline
from retrievers.retriever import Retriever
from vectorstores.faiss_store import FAISSVectorStore


class RAGService:
    def __init__(self, settings=None):
        print("Loading Smart Research Assistant...")
        settings = settings or {}
        retrieval_settings = settings.get("retrieval") or {}
        model_settings = settings.get("models") or {}
        generation_settings = settings.get("generation") or {}

        self.embedding_model = EmbeddingModel(model_name=model_settings.get("embedding_model"))
        self.vector_store = FAISSVectorStore.load(FAISS_STORAGE_PATH)
        self.retriever = Retriever(
            self.embedding_model,
            self.vector_store,
            top_k=retrieval_settings.get("top_k") or None,
        )
        llm_settings = {k: v for k, v in {
            "model": model_settings.get("llm_model"),
            "temperature": generation_settings.get("temperature"),
            "max_tokens": generation_settings.get("max_tokens"),
        }.items() if v is not None}
        self.rag = RAGPipeline(self.retriever, llm_settings=llm_settings)

        print("System Ready!")

    def ask(self, question):
        return self.rag.ask(question)

    def get_chunk_count(self):
        return len(self.vector_store.documents)
