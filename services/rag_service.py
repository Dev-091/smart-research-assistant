from config import FAISS_STORAGE_PATH

from embeddings.embedding_model import EmbeddingModel
from rag.pipeline import RAGPipeline
from retrievers.retriever import Retriever
from vectorstores.faiss_store import FAISSVectorStore


class RAGService:
    def __init__(self):
        print("Loading Smart Research Assistant...")

        self.embedding_model = EmbeddingModel()
        self.vector_store = FAISSVectorStore.load(FAISS_STORAGE_PATH)
        self.retriever = Retriever(self.embedding_model, self.vector_store)
        self.rag = RAGPipeline(self.retriever)

        print("System Ready!")

    def ask(self, question):
        return self.rag.ask(question)

    def get_chunk_count(self):
        return len(self.vector_store.documents)
