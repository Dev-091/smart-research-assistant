import faiss
import numpy as np
import pickle
import os


class FAISSVectorStore:

    def __init__(self, dimension):

        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []

    def add_documents(self, embeddings, documents):

        self.index.add(
            np.array(embeddings, dtype=np.float32)
        )

        self.documents.extend(documents)

    def similarity_search(self, query_embedding, k=3):

        distances, indices = self.index.search(
            np.array([query_embedding], dtype=np.float32),
            k
        )

        results = []

        for idx in indices[0]:
            results.append(self.documents[idx])

        return results

    def save(self, path):

        os.makedirs(path, exist_ok=True)

        faiss.write_index(
            self.index,
            os.path.join(path, "faiss.index")
        )

        with open(
            os.path.join(path, "documents.pkl"),
            "wb"
        ) as f:
            pickle.dump(self.documents, f)

    @classmethod
    def load(cls, path):

        index = faiss.read_index(
            os.path.join(path, "faiss.index")
        )

        with open(
            os.path.join(path, "documents.pkl"),
            "rb"
        ) as f:
            documents = pickle.load(f)

        obj = cls(index.d)

        obj.index = index
        obj.documents = documents

        return obj