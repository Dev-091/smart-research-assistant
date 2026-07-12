# Smart Research Assistant

A polished Retrieval-Augmented Generation (RAG) assistant designed to help you search, analyze, and summarize documents with AI-powered semantic retrieval.

## Key Technologies

- Python 3.11+
- LangChain
- FAISS vector search
- Sentence Transformers embeddings
- Groq LLM integration
- Streamlit UI for interactive use

## What This Project Does

This repo provides a complete workflow for building a research assistant that can:

- load PDF documents
- split text into searchable chunks
- generate vector embeddings
- index embeddings with FAISS
- perform semantic retrieval
- build prompts for an LLM
- answer questions using retrieved context

## User Interface

The Streamlit-based frontend is available in `app.py` and offers:

- a drag-and-drop / file upload interface for PDFs
- document preprocessing status
- semantic search and chat-style Q&A
- real-time model responses
- support for both searching and summarizing research content

> Note: The Streamlit UI is currently in active development and improving with each update.

## Project Setup

### Requirements

- Python 3.11 or newer
- `pip` package manager
- A virtual environment (recommended)

### Install Dependencies

```powershell
cd C:\Users\devsh\Desktop\smart-research-assistant
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run the Application

```powershell
streamlit run app.py
```

Then open the local URL shown in the terminal to access the UI.

### Build Index / Data Preparation

To prepare documents and build the vector index, use:

```powershell
python build_index.py
```

## Development Notes

- `loaders/pdf_loader.py` handles PDF reading
- `splitters/text_splitter.py` performs chunking
- `embeddings/embedding_model.py` builds semantic vectors
- `vectorstores/faiss_store.py` manages FAISS indexing
- `services/rag_service.py` orchestrates retrieval and LLM prompts

## Project Status

- Backend: Completed ✅
- Streamlit frontend: In Progress 🚧

## Contribution

Contributions and improvements are welcome. Feel free to open issues or submit pull requests for:

- better UI flow
- expanded document loader support
- enhanced prompt templates
- model / configuration options
