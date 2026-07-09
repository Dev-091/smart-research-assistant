from config import PDF_PATH, FAISS_STORAGE_PATH

from loaders.pdf_loader import load_pdf
from splitters.text_splitter import split_documents
from embeddings.embedding_model import EmbeddingModel
from vectorstores.faiss_store import FAISSVectorStore


def build_index():

    print("=" * 60)
    print("Building Knowledge Base...")
    print("=" * 60)

    # Step 1: Load PDF
    documents = load_pdf(PDF_PATH)

    print(f"Loaded {len(documents)} pages.")

    # Step 2: Split Documents
    chunks = split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    # Step 3: Load Embedding Model
    embedding_model = EmbeddingModel()

    # Step 4: Generate Embeddings
    embeddings = embedding_model.embed_documents(chunks)

    print("Embeddings generated.")

    # Step 5: Create FAISS
    vector_store = FAISSVectorStore(
        embeddings.shape[1]
    )

    # Step 6: Store Vectors
    vector_store.add_documents(
        embeddings,
        chunks
    )

    # Step 7: Save
    vector_store.save(
        FAISS_STORAGE_PATH
    )

    print()
    print("Knowledge Base Created Successfully!")
    print(f"Saved to: {FAISS_STORAGE_PATH}")


if __name__ == "__main__":
    build_index()