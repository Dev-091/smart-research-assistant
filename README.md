# Smart Research Assistant

A RAG-based document assistant for uploading PDFs, building a local vector index, and asking grounded questions with source-backed responses.

## What This Project Matches From The Brief

This repo implements the core workflow described in the project PDF:

- document upload and processing
- chunking and embedding generation
- FAISS-based vector storage
- semantic retrieval
- prompt-based answer generation
- evaluation with RAG-style metrics
- Streamlit chat UI

## Workflow

### 1. Data Ingestion
- PDFs are uploaded through the Streamlit sidebar.
- Files are stored in `data/raw/`.
- The knowledge base is rebuilt from all PDFs in that folder.

### 2. Indexing
- `build_index.py` loads each PDF.
- Documents are split into chunks.
- Chunks are embedded with Sentence Transformers.
- Embeddings and chunk metadata are saved into FAISS.

### 3. Retrieval
- User questions are embedded.
- The top-k nearest chunks are retrieved from FAISS.
- Retrieved context is passed into the prompt builder.

### 4. Answer Generation
- The LLM receives the question plus retrieved context.
- The answer is generated only from the retrieved material.
- Sources are shown in the UI with page numbers and chunk previews.

### 5. Evaluation
- `evaluation/ragas_eval.py` evaluates answer correctness, context alignment, and overall quality.
- A benchmark file in `evaluation/benchmark.json` defines the test questions.

## UI

The Streamlit frontend includes:

- PDF upload and document management
- build/rebuild knowledge base controls
- settings for retrieval, chunking, and generation
- chat-style Q&A with source citations
- response timing and chat export

## Tech Stack

- Python
- Streamlit
- LangChain
- FAISS
- Sentence Transformers
- Groq LLM API
- RAGAS for evaluation

## Evaluation

The evaluation module is designed to match the brief:

- `answer_correctness` measures whether the generated answer matches the expected answer.
- `context_alignment` measures whether the retrieved context supports the expected answer.
- `overall_quality` combines the two into one project-level score.

If the full RAGAS stack is available in the environment, the evaluator uses the real library. Otherwise, it falls back to a local approximation so the workflow remains runnable.

## Important Note On The Brief

The PDF also mentions some future or optional ideas that are not fully implemented in the current codebase yet:

- TXT and web content ingestion
- switching between FAISS and ChromaDB in the UI
- Gradio frontend
- multi-turn memory beyond Streamlit session chat history
- highlight-based document section viewer
- cloud deployment and authentication

Those are good next-step enhancements, but the current codebase focuses on the PDF-first Streamlit RAG workflow.

## Project Setup

### Requirements

- Python 3.11 or newer
- `pip` package manager
- A virtual environment is recommended

### Install Dependencies

```powershell
cd C:\Users\devsh\Desktop\smart-research-assistant
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run the App

```powershell
streamlit run app.py
```

### Build The Index

```powershell
python build_index.py
```

### Run Evaluation

```powershell
python evaluation\ragas_eval.py
```

## Project Structure

- `loaders/` handles document loading
- `splitters/` handles chunking
- `embeddings/` handles embeddings
- `vectorstores/` handles FAISS storage
- `retrievers/` handles retrieval
- `llm/` handles prompt building and generation
- `rag/` orchestrates the full pipeline
- `services/` contains frontend and app services
- `components/` contains Streamlit UI modules
- `evaluation/` contains the RAG benchmark and scoring script

## Status

- Backend: completed
- Frontend: modular and in progress toward production polish
- Evaluation: implemented with RAGAS-compatible scoring
