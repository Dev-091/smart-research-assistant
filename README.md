# 🧠 Smart Research Assistant

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-121212?style=for-the-badge)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Store-green?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-Fast_LLM-f55036?style=for-the-badge)

A powerful **Retrieval-Augmented Generation (RAG)** document assistant that allows you to upload PDFs, build a local vector knowledge base, and chat with your documents. Ask complex questions and get grounded, source-backed responses instantly.

---

## ✨ Features

- **📄 Document Management:** Upload and manage multiple PDF documents directly from the UI.
- **🔍 Semantic Retrieval:** High-performance vector similarity search powered by FAISS and Hugging Face `SentenceTransformers`.
- **💬 Conversational Memory:** Context-aware multi-turn chat allowing you to ask seamless follow-up questions.
- **📝 Source Citations:** Every generated answer is backed by direct citations to the source documents, complete with page numbers and visually highlighted text snippets.
- **⚙️ Dynamic Configuration:** Tweak chunk sizes, retrieval `top_k`, temperature, and embedding models on the fly.
- **📊 Automated Evaluation:** Built-in integration with **RAGAS** to evaluate answer correctness, context alignment, and overall quality natively within the UI.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Orchestration:** LangChain
- **Vector Database:** FAISS
- **Embeddings:** Hugging Face `SentenceTransformers` (`all-mpnet-base-v2` / `all-MiniLM-L6-v2`)
- **LLM:** Groq API (`llama-3.3-70b-versatile` / `mixtral-8x7b-32768`)
- **Evaluation:** Ragas

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.11 or newer
- `pip` package manager
- A valid [Groq API Key](https://console.groq.com/) for LLM generation.

### 2. Installation
Clone the repository and set up a virtual environment:

```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run the Application
Launch the Streamlit interface:
```powershell
streamlit run app.py
```

---

## 🏗️ Architecture & Structure

The repository is modularized for enterprise scalability:

```text
smart-research-assistant/
├── app.py                  # Main Streamlit application entry point
├── build_index.py          # CLI script for building the knowledge base
├── components/             # Streamlit UI modules (sidebar, chat panel)
├── embeddings/             # Embedding model wrappers
├── evaluation/             # RAGAS automated scoring scripts
├── llm/                    # LLM clients and prompt builders
├── loaders/                # Document ingestion (PyPDFLoader)
├── rag/                    # Retrieval-Augmented Generation pipeline orchestration
├── retrievers/             # Search logic against vector stores
├── services/               # State management and UI logic decoupling
├── splitters/              # Text chunking logic
└── vectorstores/           # FAISS index management
```

---

## 🧪 Evaluation Pipeline

This project features a native evaluation loop using **RAGAS**. You can trigger the evaluation directly from the UI to assess the current knowledge base against a benchmark dataset (`evaluation/benchmark.json`). 

The evaluation calculates:
1. **Answer Correctness:** Does the LLM answer match the ground truth?
2. **Context Alignment:** Is the retrieved context actually relevant to the question?
3. **Overall Quality:** A balanced score of correctness and context alignment.

---
*Built for fast, accurate, and source-backed AI research.*
