from config import PDF_PATH

from loaders.pdf_loader import load_pdf
from splitters.text_splitter import split_documents
from embeddings.embedding_model import EmbeddingModel
from vectorstores.faiss_store import FAISSVectorStore
from retrievers.retriever import Retriever


documents = load_pdf(PDF_PATH)

chunks = split_documents(documents)

embedding_model = EmbeddingModel()

embeddings = embedding_model.embed_documents(chunks)

vector_store = FAISSVectorStore(
    embeddings.shape[1]
)

vector_store.add_documents(
    embeddings,
    chunks
)

retriever = Retriever(
    embedding_model,
    vector_store
)

results = retriever.retrieve(
    "software developer"
)

print()

for i, doc in enumerate(results):

    print("=" * 60)

    print(f"Result {i+1}")

    print(doc.page_content[:300])

    print()

    print(doc.metadata)