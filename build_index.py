from pathlib import Path

from config import FAISS_STORAGE_PATH, PDF_PATH, RAW_DATA_DIR

from embeddings.embedding_model import EmbeddingModel
from loaders.pdf_loader import load_pdfs
from splitters.text_splitter import split_documents
from vectorstores.faiss_store import FAISSVectorStore


def _resolve_pdf_paths(pdf_path=None):
    if pdf_path is not None:
        path = Path(pdf_path)
        return [path]

    raw_directory = Path(RAW_DATA_DIR)
    pdf_paths = sorted(raw_directory.glob("*.pdf"))
    if pdf_paths:
        return pdf_paths

    return [Path(PDF_PATH)]


def build_index(pdf_path=None, settings=None):
    settings = settings or {}
    chunk_settings = settings.get("chunking") or {}
    model_settings = settings.get("models") or {}

    pdf_paths = _resolve_pdf_paths(pdf_path)
    if not pdf_paths:
        raise FileNotFoundError("No PDF files were found to build the knowledge base.")

    print("=" * 60)
    print("Building Knowledge Base...")
    print("=" * 60)

    documents = load_pdfs(pdf_paths)
    print(f"Loaded {len(documents)} pages from {len(pdf_paths)} document(s).")

    chunks = split_documents(
        documents,
        chunk_size=chunk_settings.get("chunk_size"),
        chunk_overlap=chunk_settings.get("chunk_overlap"),
    )
    print(f"Created {len(chunks)} chunks.")

    embedding_model = EmbeddingModel(model_name=model_settings.get("embedding_model"))
    embeddings = embedding_model.embed_documents(chunks)
    print("Embeddings generated.")

    vector_store = FAISSVectorStore(embeddings.shape[1])
    vector_store.add_documents(embeddings, chunks)
    vector_store.save(FAISS_STORAGE_PATH)

    summary = {
        "document_count": len(pdf_paths),
        "page_count": len(documents),
        "chunk_count": len(chunks),
        "storage_path": FAISS_STORAGE_PATH,
        "document_names": [path.name for path in pdf_paths],
        "settings": settings,
    }

    print()
    print("Knowledge Base Created Successfully!")
    print(f"Saved to: {FAISS_STORAGE_PATH}")

    return summary


if __name__ == "__main__":
    build_index()
