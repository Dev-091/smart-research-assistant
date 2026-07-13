from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_OVERLAP, CHUNK_SIZE


def split_documents(documents, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks = text_splitter.split_documents(documents)

    return chunks
