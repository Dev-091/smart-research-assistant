from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

class EmbeddingModel:

    def __init__(self, model_name=EMBEDDING_MODEL):
        print("Loading embedding model...")

        self.model = SentenceTransformer(model_name)

        print("Embedding model loaded successfully!")

    def embed_documents(self, documents):
    
        texts = [doc.page_content for doc in documents]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True,
        )

        return embeddings

    def embed_query(self, query):
        
        embedding = self.model.encode(
            query,
            convert_to_numpy=True,
        )

        return embedding