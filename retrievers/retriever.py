from config import TOP_K


class Retriever:

    def __init__(
        self,
        embedding_model,
        vector_store
    ):

        self.embedding_model = embedding_model

        self.vector_store = vector_store

    def retrieve(
        self,
        query,
        k=TOP_K
    ):

        query_embedding = self.embedding_model.embed_query(
            query
        )

        documents = self.vector_store.similarity_search(
            query_embedding,
            k
        )

        return documents