from loaders.pdf_loader import load_pdf
from splitters.text_splitter import split_documents
from embeddings.embedding_model import EmbeddingModel
from vectorstores.faiss_store import FAISSVectorStore

documents = load_pdf("data/raw/sample.pdf")

chunks = split_documents(documents)

embedding_model = EmbeddingModel()

embeddings = embedding_model.embed_documents(chunks)

dimension = embeddings.shape[1]

store = FAISSVectorStore(dimension)

store.add_documents(

    embeddings,

    chunks

)

query = "software developer"

query_embedding = embedding_model.embed_query(query)

results = store.similarity_search(

    query_embedding,

    k=3

)

print("\nTop Results\n")

for i, doc in enumerate(results):

    print("="*60)

    print(f"Result {i+1}")

    print(doc.page_content[:300])

    print("\nPage:", doc.metadata["page"]+1)