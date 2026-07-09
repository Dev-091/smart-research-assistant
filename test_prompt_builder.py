from config import PDF_PATH

from loaders.pdf_loader import load_pdf
from splitters.text_splitter import split_documents
from embeddings.embedding_model import EmbeddingModel
from vectorstores.faiss_store import FAISSVectorStore
from retrievers.retriever import Retriever
from llm.prompt_builder import PromptBuilder

documents = load_pdf(PDF_PATH)

chunks = split_documents(documents)

embedding_model = EmbeddingModel()

embeddings = embedding_model.embed_documents(chunks)

vector_store = FAISSVectorStore(embeddings.shape[1])

vector_store.add_documents(
    embeddings,
    chunks
)

retriever = Retriever(
    embedding_model,
    vector_store
)

results = retriever.retrieve(
    "What programming websites should I practice?"
)

prompt_builder = PromptBuilder()

prompt = prompt_builder.build_prompt(
    "What programming websites should I practice?",
    results
)

print(prompt)