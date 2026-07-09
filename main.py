from config import FAISS_STORAGE_PATH

from embeddings.embedding_model import EmbeddingModel
from vectorstores.faiss_store import FAISSVectorStore
from retrievers.retriever import Retriever
from rag.pipeline import RAGPipeline


def main():

    print("=" * 60)
    print("Smart Research Assistant")
    print("=" * 60)

    print("\nLoading Embedding Model...")

    embedding_model = EmbeddingModel()

    print("\nLoading Knowledge Base...")

    vector_store = FAISSVectorStore.load(
        FAISS_STORAGE_PATH
    )

    print("Knowledge Base Loaded Successfully!")

    retriever = Retriever(
        embedding_model,
        vector_store
    )

    rag = RAGPipeline(
        retriever
    )

    print("\nAssistant Ready!")
    print("Type 'exit' to quit.\n")

    while True:

        query = input("You : ")

        if query.lower() == "exit":
            break

        print("\nSearching...\n")

        answer = rag.ask(query)

        print("Assistant :\n")

        print(answer)

        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()