import pickle
from pathlib import Path

from build_index import build_index
from config import FAISS_STORAGE_PATH, RAW_DATA_DIR


class DocumentManager:
    def __init__(self, raw_data_dir=RAW_DATA_DIR, storage_path=FAISS_STORAGE_PATH):
        self.raw_data_dir = Path(raw_data_dir)
        self.storage_path = Path(storage_path)
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def save_uploaded_files(self, uploaded_files):
        saved_files = []

        for uploaded_file in uploaded_files:
            target_path = self.raw_data_dir / Path(uploaded_file.name).name
            target_path.write_bytes(uploaded_file.getbuffer())
            saved_files.append(target_path.name)

        if saved_files:
            self.invalidate_index()

        return saved_files

    def list_documents(self):
        documents = []

        for file_path in sorted(self.raw_data_dir.glob("*.pdf")):
            documents.append(
                {
                    "name": file_path.name,
                    "size_mb": round(file_path.stat().st_size / (1024 * 1024), 2),
                }
            )

        return documents

    def delete_document(self, document_name):
        file_path = self.raw_data_dir / Path(document_name).name
        if file_path.exists():
            file_path.unlink()
            self.invalidate_index()
            return True
        return False

    def delete_all_documents(self):
        deleted_count = 0
        for file_path in self.raw_data_dir.glob("*.pdf"):
            file_path.unlink()
            deleted_count += 1

        if deleted_count:
            self.invalidate_index()

        return deleted_count

    def invalidate_index(self):
        for file_name in ["documents.pkl", "faiss.index"]:
            file_path = self.storage_path / file_name
            if file_path.exists():
                file_path.unlink()

    def build_knowledge_base(self):
        return build_index()

    def get_index_stats(self):
        stats = {
            "document_count": len(self.list_documents()),
            "chunk_count": 0,
            "index_ready": False,
        }

        documents_pickle = self.storage_path / "documents.pkl"
        faiss_index = self.storage_path / "faiss.index"
        if documents_pickle.exists() and faiss_index.exists():
            with documents_pickle.open("rb") as file:
                stored_documents = pickle.load(file)
            stats["chunk_count"] = len(stored_documents)
            stats["index_ready"] = True

        return stats
