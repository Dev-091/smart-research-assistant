from config import TOP_K


class Retriever:
    def __init__(self, embedding_model, vector_store, top_k=TOP_K):
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.top_k = top_k or TOP_K

    def retrieve(self, query, k=None):
        query_embedding = self.embedding_model.embed_query(query)
        documents = self.vector_store.similarity_search(
            query_embedding,
            k or self.top_k,
        )
        return documents
