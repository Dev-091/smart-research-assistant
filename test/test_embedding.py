from loaders.pdf_loader import load_pdf
from splitters.text_splitter import split_documents
from embeddings.embedding_model import EmbeddingModel

documents = load_pdf("data/raw/sample.pdf")

chunks = split_documents(documents)

embedding_model = EmbeddingModel()

embeddings = embedding_model.embed_documents(chunks)

print("\nTotal Chunks :", len(chunks))

print("Total Embeddings :", len(embeddings))

print("Embedding Dimension :", len(embeddings[0]))

print("\nFirst 10 values")

print(embeddings[0][:10])

query = "What is software development?"

query_embedding = embedding_model.embed_query(query)

print("\nQuery Dimension :", len(query_embedding))