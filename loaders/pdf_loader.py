from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader


def load_pdf(file_path):
    loader = PyPDFLoader(str(file_path))
    documents = loader.load()
    return documents


def load_pdfs(file_paths):
    all_documents = []

    for file_path in file_paths:
        documents = load_pdf(file_path)
        source_name = Path(file_path).name

        for document in documents:
            document.metadata["document_name"] = source_name

        all_documents.extend(documents)

    return all_documents
