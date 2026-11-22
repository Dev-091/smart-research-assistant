# Smart Research Assistant — Viva Guide

This guide explains the project in simple language and follows the code that is
currently in this repository. It includes a short presentation, the file
structure, both data flows, important concepts, limitations, and likely viva
questions with direct answers.

## 1. Project in one sentence

**Smart Research Assistant is a web app that lets a user upload PDF research
documents, search their content by meaning, and ask an AI questions answered
using relevant parts of those documents.**

The project uses Retrieval-Augmented Generation (RAG): it retrieves relevant
text first, then gives that text to a language model to help produce an answer.

## 2. Short viva introduction

> My project is called Smart Research Assistant. It helps users ask questions
> about PDF documents. When a PDF is added, the app extracts its text, divides
> the text into smaller overlapping sections, converts each section into a
> numerical meaning representation called an embedding, and saves those
> embeddings in a FAISS index. When the user asks a question, the app embeds the
> question, finds the closest document sections, and sends those sections with
> the question to an LLM through Groq. The answer is shown with source details
> such as the document name and page. The interface is built with Streamlit.
> This approach is useful because the model receives focused evidence instead
> of the whole document, and the document can be updated without retraining the
> LLM.

If asked what you personally built, describe the parts you actually worked on.
The codebase includes the Streamlit interface, PDF ingestion, chunking,
embeddings, FAISS storage, retrieval, LLM prompting, citations, settings, and
an evaluation module.

## 3. Problem and solution

### Problem

Reading long research PDFs takes time. A normal chatbot may also answer from
general knowledge rather than from the particular document a user wants to
understand.

### Solution

The app prepares searchable PDF content in advance. For each question it finds
the most relevant parts and asks the LLM to answer from that context. The app
also shows the source pages so the user can check the answer.

### Main goals

- Make it easier to ask questions about one or more PDFs.
- Find useful passages by meaning, not only exact keyword matches.
- Keep answers tied to the uploaded documents.
- Show source document and page information for checking.
- Let the user adjust important retrieval and generation settings.

## 4. Why use RAG instead of sending the whole document to an LLM?

This is a common viva question. A good short answer is:

> I do not send the whole document for every question because a document can be
> too large for the model's context limit, and sending all of it uses more
> tokens, time, and API cost. It also gives the model lots of irrelevant text.
> RAG searches for the few sections that best match the question and sends only
> those sections. It makes answers more focused and gives us source information.

More detail, if asked:

1. **Context size:** Long PDFs can exceed the number of tokens the model accepts
   in one request. Splitting and retrieving helps work with larger files.
2. **Cost and speed:** Sending less text usually means fewer input tokens and
   less work per question. Indexing has an initial cost, but the prepared index
   can be reused for later questions.
3. **Relevance:** A whole document contains details unrelated to the question.
   Retrieval tries to supply the most relevant chunks.
4. **Grounding:** The prompt tells the model to answer only from the provided
   context and gives a fixed response when the context lacks the answer.
5. **Updating documents:** The user can rebuild the index after changing PDFs;
   the underlying LLM does not have to be retrained.
6. **Sources:** Retrieved chunks retain document and page metadata, which the
   app can show alongside the answer.

**Be accurate:** RAG can reduce unsupported answers, but it does not guarantee
that every answer is correct. Retrieval can miss useful text, and an LLM can
still misunderstand the context. The user should check the sources.

## 5. Technologies and what each does

| Technology | Use in this project |
| --- | --- |
| Python | Main programming language |
| Streamlit | Web interface, upload controls, settings, chat, and display |
| PyPDFLoader / pypdf | Reads PDF pages and extracts text |
| RecursiveCharacterTextSplitter | Divides page text into smaller overlapping chunks |
| Sentence Transformers | Converts document text and questions into embeddings |
| FAISS | Stores and searches chunk vectors locally |
| Groq API | Sends prompts to a hosted language model and receives answers |
| LangChain packages | Document loading and text splitting helpers |
| RAGAS (optional path) | Provides LLM/RAG evaluation metrics when available |
| JSON / pickle / FAISS files | Save settings, document chunks, and the vector index |

The defaults in `config.py` include a chunk size of 500 characters, overlap of
100 characters, top-k of 3, the `all-MiniLM-L6-v2` embedding model, temperature
0, and a maximum of 1024 generated tokens. Settings can be changed through the
sidebar and saved. Do not claim that every run uses these defaults: saved
settings can override them.

## 6. Project file structure

### Main files

- [`app.py`](./app.py) — Streamlit entry point. Sets up the page, renders the
  app, processes sidebar actions, and runs index building/evaluation actions.
- [`build_index.py`](./build_index.py) — Ingestion/index-building process:
  loads PDFs, chunks text, makes embeddings, and saves the vector store.
- [`main.py`](./main.py) — A separate basic command-line chat entry point that
  loads an existing index. The main user-facing app is `app.py`.
- [`config.py`](./config.py) — Default values for paths, chunking, retrieval,
  embedding, and LLM generation.
- [`requirements.txt`](./requirements.txt) — Runtime Python dependencies.
- [`README.md`](./README.md) — Setup and high-level project description. Some
  descriptive text may not reflect every detail of the current implementation;
  for implementation questions, follow the Python source.

### Application interface

- [`components/header.py`](./components/header.py) — Renders the top header.
- [`components/sidebar.py`](./components/sidebar.py) — Upload controls,
  document listing, settings, system stats, evaluation button, and chat/theme
  controls.
- [`components/chat.py`](./components/chat.py) — Displays chat messages,
  accepts the question, calls the RAG service, and shows sources and downloads.
- [`styles/style.css`](./styles/style.css) — Visual styling for the interface.

### Backend building blocks

- [`loaders/pdf_loader.py`](./loaders/pdf_loader.py) — Loads pages from PDF
  files and records the source PDF name in metadata.
- [`splitters/text_splitter.py`](./splitters/text_splitter.py) — Splits loaded
  pages into chunks.
- [`embeddings/embedding_model.py`](./embeddings/embedding_model.py) — Creates
  embeddings for chunks and questions.
- [`vectorstores/faiss_store.py`](./vectorstores/faiss_store.py) — Adds vectors
  to FAISS, searches them, and saves/loads the index and chunk documents.
- [`retrievers/retriever.py`](./retrievers/retriever.py) — Provides a reusable
  retrieval helper. The main `RAGPipeline` currently performs its scored search
  through the vector store directly.
- [`rag/pipeline.py`](./rag/pipeline.py) — Connects question handling,
  retrieval, prompt creation, LLM generation, and source metadata.
- [`llm/prompt_builder.py`](./llm/prompt_builder.py) — Builds the grounded
  prompt, conversational question-rewrite prompt, and citation metadata.
- [`llm/llm_client.py`](./llm/llm_client.py) — Calls the Groq chat completion
  API using the key in the environment.

### Services and data

- [`services/document_manager.py`](./services/document_manager.py) — Saves,
  lists, and deletes PDF uploads; removes an old index when documents change;
  starts index building.
- [`services/rag_service.py`](./services/rag_service.py) — Loads the embedding
  model and saved FAISS data, then exposes the question-answering service.
- [`services/app_settings.py`](./services/app_settings.py) — Loads, saves, and
  normalizes settings.
- [`services/frontend_state.py`](./services/frontend_state.py) — Manages
  Streamlit session state and lazily loads the RAG service when an index exists.
- [`evaluation/ragas_eval.py`](./evaluation/ragas_eval.py) — Runs benchmark
  questions and calculates metrics.
- [`evaluation/benchmark.json`](./evaluation/benchmark.json) — Example
  questions, expected answers, and expected source names.
- [`test/`](./test) — Small scripts for trying the loader, splitter, embedding,
  FAISS, retriever, prompt builder, and LLM.
- [`data/raw/`](./data/raw) — PDFs provided to or uploaded into the app.
- [`storage/`](./storage) — Saved FAISS index, serialized chunk documents, and
  application settings.
- [`data/processed/`](./data/processed) — Directory reserved for processed
  data; the active index persistence in this implementation is under `storage/`.

The project also has `embeddings/`, `loaders/`, `llm/`, `rag/`, `retrievers/`,
`splitters/`, `vectorstores/`, `components/`, `services/`, and `evaluation/`
Python packages. Their `__init__.py` files mark the directories as packages.

## 7. How to run and demonstrate it

The README's basic setup is:

1. Create and activate a Python virtual environment.
2. Install the packages from `requirements.txt`.
3. Put a valid Groq key in a local `.env` file as `GROQ_API_KEY=...`.
4. Start the interface with `streamlit run app.py`.
5. Upload a PDF in the sidebar, save it, and select **Build Knowledge Base**.
6. Ask a question in the chat and open **Sources** to inspect the retrieved
   pages.

For a viva demonstration, choose a question whose answer is clearly present in
the uploaded PDF. Show the uploaded-document count, build the index, ask the
question, then point to the answer and source page. If asked, change `top_k` or
the chunk settings and explain that indexing settings need a rebuild to affect
the existing index. Evaluation can be run from its sidebar control, but it
requires the saved knowledge base and may need optional RAGAS dependencies.

## 8. Data flow: building the knowledge base

This is the **offline or setup flow**. It happens when the user saves PDFs and
chooses to build or rebuild the knowledge base.

```text
PDF upload in Streamlit
    ↓
DocumentManager saves PDF(s) under data/raw/
    ↓
build_index.py finds the PDF files
    ↓
PyPDFLoader reads each page and its metadata
    ↓
RecursiveCharacterTextSplitter creates overlapping chunks
    ↓
SentenceTransformer converts each chunk to a vector
    ↓
FAISS stores the vectors; chunk documents stay aligned by index
    ↓
storage/faiss.index + storage/documents.pkl are saved
```

In more detail:

1. The sidebar accepts PDF files. The app saves the file content through
   `DocumentManager`.
2. Saving or deleting a PDF invalidates the existing index files, because the
   index no longer represents the current set of documents.
3. `build_index()` searches the raw data directory for PDFs. If that directory
   has no PDFs, it uses the configured fallback PDF path.
4. `load_pdfs()` gets page documents from `PyPDFLoader`. It adds
   `document_name` metadata; the loader also supplies the page metadata.
5. The recursive splitter uses configured chunk size and overlap. The overlap
   keeps some text from one chunk in the next, which helps avoid losing context
   at chunk boundaries.
6. The embedding model converts every chunk to a numeric vector.
7. `FAISSVectorStore` creates a flat L2 index, stores the vectors as
   32-bit floating-point numbers, and keeps the corresponding chunk documents
   in a Python list.
8. The app persists the FAISS index and document list as
   `storage/faiss.index` and `storage/documents.pkl`.

## 9. Data flow: asking a question

This is the **online question-answering flow**.

```text
User asks a question in the chat
    ↓
Streamlit passes question and conversation history to RAGService
    ↓
RAGPipeline makes a standalone search question if history is present
    ↓
EmbeddingModel turns the search question into a vector
    ↓
FAISS returns the top-k closest chunks and their L2 distances
    ↓
PromptBuilder combines retrieved chunks, history, and the user's question
    ↓
LLMClient sends the prompt to Groq
    ↓
Answer + source metadata return to Streamlit
    ↓
Chat shows answer, page/source details, elapsed time, and a JSON download
```

In more detail:

1. `RAGService` loads the embedding model and the saved index. The frontend
   checks that both saved index files exist before trying to initialize this
   service.
2. If there is chat history, the pipeline asks the LLM to rewrite a follow-up
   question as a standalone search query. This helps with questions such as
   “What about its limitations?” where “its” refers to something from earlier.
3. The embedding model embeds that search query.
4. FAISS finds up to `top_k` vectors with the smallest L2 distances. The default
   `top_k` is 3.
5. The prompt builder includes each retrieved chunk and its page number, the
   recent chat history (up to five messages), and the original question.
6. The prompt instructs the model to use only the supplied context and to
   return a specific “couldn't find that information” response if the answer
   is absent.
7. The LLM client calls Groq. The API key is read from the `GROQ_API_KEY`
   environment variable (commonly loaded from a local `.env` file).
8. The pipeline returns an answer and separate source metadata. The UI displays
   the answer, source page/document name, a chunk preview, and a score. It can
   also provide a JSON download of the question, answer, sources, and response
   time.

## 10. Important concepts in plain language

- **LLM:** A language model that can read a prompt and generate text. It
  generates the final answer here; it does not perform the PDF search itself.
- **Embedding:** A list of numbers representing the meaning of a piece of
  text. Texts with related meanings often have vectors that are close together.
- **Vector store:** A system for storing vectors and finding nearby vectors.
  This project uses FAISS.
- **Chunk:** A smaller piece of a document. The app searches these rather than
  comparing a question with an entire PDF.
- **Chunk overlap:** Text repeated at a chunk boundary so a sentence or idea is
  less likely to be split apart without surrounding context.
- **Retriever:** The component that finds document chunks relevant to a
  question.
- **Prompt:** The instructions and information sent to the LLM.
- **Grounding:** Giving the model relevant source text and directing it to base
  its answer on that text.
- **Top-k:** How many nearest chunks to retrieve. A larger value may include
  more evidence, but can also add irrelevant text and use more tokens.
- **Temperature:** A generation setting that affects variation. Lower values
  generally make responses less varied; the default here is 0.
- **Metadata:** Extra information attached to a page/chunk, such as its page
  number and source document name.

### How to explain the vector search score correctly

The FAISS index is `IndexFlatL2`, so the returned value is an **L2 distance**,
not a percentage and not a conventional “higher means more similar” score.
Smaller distance means a closer vector under this index. The UI labels it
“Score,” but do not describe it as a probability or a similarity percentage.

## 11. Design choices: likely “why” questions

### Why use chunks?

> A PDF can be very long. Chunks make it possible to search smaller pieces,
> return only useful evidence, and stay within the LLM's prompt limit.

### Why use overlap?

> An idea can cross a chunk boundary. Overlap repeats a small amount of text so
> the next chunk still has some of the previous context.

### Why embeddings instead of exact keyword search?

> Embeddings let the app search for related meaning even when the question and
> document use different words. For example, “car” and “vehicle” may be related.
> This is semantic similarity, not a guarantee of understanding.

### Why FAISS?

> FAISS is a practical local library for nearest-vector search. It avoids
> requiring a separate vector database server for this project and can search
> the stored vectors efficiently.

### Why use a separate embedding model and LLM?

> The embedding model is used to represent text for search. The LLM is used to
> understand the retrieved context and generate a readable response. These are
> two different tasks.

### Why save an index?

> The app can reuse the PDF chunks and their vectors for later questions instead
> of parsing and embedding every PDF again each time.

### Why use metadata?

> Metadata lets the app identify which PDF and page supplied a retrieved chunk,
> so the user can trace the answer back to the source.

### Why keep the API key in an environment variable?

> It avoids putting the secret key directly in the source code. The running app
> reads the key from its environment.

## 12. Citations: what the project does and does not do

The app returns a source list separately from the answer. Each source record
can include its document name, 1-based page number, the first part of the chunk,
and the FAISS distance.

The retrieved context is labelled “Source 1,” “Source 2,” and so on inside the
prompt. However, the app does **not** force the LLM to insert formal citation
markers such as `[1]` into every sentence. The UI presents the source list
separately. Explain it as “source information is shown with the answer,” not as
“every sentence has a verified citation.”

## 13. Settings and saved data

- Settings are managed by `AppSettingsService`, merged with defaults, and
  normalized before saving.
- The sidebar exposes retrieval count, chunk size and overlap, embedding model,
  LLM model, temperature, and maximum output tokens.
- Changing an embedding model requires rebuilding the index so document and
  question vectors use the same model.
- Changing chunking settings also requires rebuilding the index to apply them
  to existing PDFs.
- The FAISS index is saved separately from the pickled chunk documents. Both
  are needed to load the knowledge base.
- The Groq API key is not an app setting; it is read from `GROQ_API_KEY`.
- Chat messages and theme are kept in Streamlit session state. The code does
  not implement a permanent chat-history database.

## 14. Evaluation

The evaluation module reads question/answer examples from
`evaluation/benchmark.json`. For each benchmark question, it asks the RAG
service for an answer and measures response time and answer/context scores.

When RAGAS and its dependencies work in the environment, the module tries
RAGAS metrics including answer correctness, answer relevancy, faithfulness, and
context precision. It combines faithfulness, context precision, and answer
relevancy into the displayed context-alignment score.

If the RAGAS path cannot be imported or run, the code uses a local fallback:

- Answer correctness is based on exact normalized text and expected-answer word
  overlap.
- Context alignment is based on expected-answer word overlap with retrieved
  chunk previews.
- Overall quality is the average of those two scores.

**Important:** The fallback is a simple comparison, not a deep judgment of
meaning. Scores depend on the benchmark and should not be presented as proof
that the system is always accurate. The UI shows the metric backend used.

## 15. Limitations and honest answers

Knowing limitations makes your viva answers more credible.

1. **PDF extraction:** The current loader extracts text from PDFs. Scanned
   image-only pages may need OCR, which is not implemented in the loader.
2. **Retrieval quality:** Similarity search can miss the right chunk or return
   a related but insufficient chunk. Chunk size, overlap, embedding model, and
   top-k affect results.
3. **Generation quality:** The LLM may still misunderstand or add unsupported
   details despite the prompt instruction. Source checking remains important.
4. **Hosted LLM:** The question/context prompt is sent to Groq's API. The
   embedding and FAISS search are performed by local project code, but answer
   generation depends on network access, API availability, and a valid key.
5. **Index type:** `IndexFlatL2` performs a flat exact search. It is simple but
   can become slower as the number of vectors grows compared with approximate
   indexes or a managed vector database.
6. **Persistence:** The vector index and document objects are saved locally.
   The project does not implement a production database, user accounts, or
   multi-user access control.
7. **Citations:** The app displays retrieved sources, but does not verify each
   answer sentence against those sources.
8. **Streaming:** The chat display yields the already-generated answer a word
   at a time for presentation. The Groq client call itself requests a completed
   response rather than streaming model tokens.
9. **Testing:** The scripts in `test/` are small exploratory scripts; most print
   results rather than asserting expected behavior. Do not claim a complete
   automated test suite unless you have separately added and run one.
10. **Evaluation:** The benchmark is small and the fallback metrics are simple.
    A larger reviewed benchmark would give a more reliable quality picture.

If asked what you would improve next:

> I would add OCR support for scanned PDFs, a stronger evaluation set, robust
> automated tests, and better source-grounded citation checks. For larger
> collections I would consider an approximate or managed vector database. I
> would also add user access control and more persistent chat storage if the
> app were deployed for multiple users.

## 16. Common viva questions and direct answers

### Q1. What is the objective of this project?

**Answer:** The objective is to let people ask questions about their PDF
documents and get answers based on relevant document content, with source
information they can check.

### Q2. What does RAG stand for?

**Answer:** Retrieval-Augmented Generation. The system retrieves useful
information first and then gives it to a language model to generate an answer.

### Q3. What is the input and output?

**Answer:** The main input is one or more PDF files and a user's question. The
output is a generated answer and a list of retrieved source details.

### Q4. Explain the complete project flow.

**Answer:** PDFs are loaded, split into chunks, embedded, and saved in FAISS.
For a question, the app embeds the question, retrieves nearby chunks, puts them
in a prompt, calls the LLM, and shows the answer with source details.

### Q5. What is an embedding?

**Answer:** It is a list of numbers representing text meaning. The app compares
the question vector with document chunk vectors to find related content.

### Q6. Is the LLM searching the PDF?

**Answer:** No. The embedding model and FAISS perform retrieval. The LLM receives
the retrieved text and writes the answer.

### Q7. How is this different from ChatGPT by itself?

**Answer:** A general chatbot answers from its model knowledge and prompt. This
project first retrieves content from the user's PDFs and includes that content
as evidence in the prompt.

### Q8. Why not pass all the PDF text directly to the LLM?

**Answer:** It may be too long, cost more, take longer, and contain a lot of
irrelevant material. Retrieval sends a smaller set of passages related to the
question.

### Q9. Why split into chunks?

**Answer:** Smaller sections are easier to search and fit into the prompt. They
also let us retrieve just the relevant parts instead of whole pages or books.

### Q10. What is overlap?

**Answer:** It is text repeated between neighboring chunks. It helps preserve
context when an idea is split near a boundary.

### Q11. What happens if the answer is not in the PDF?

**Answer:** The prompt tells the LLM to say, “I couldn't find that information
in the provided document.” This reduces unsupported answers, but it is not a
perfect guarantee.

### Q12. What is top-k?

**Answer:** It is the number of closest chunks returned for a question. The
default is three, but it can be adjusted.

### Q13. What does FAISS do?

**Answer:** It stores document vectors and quickly searches for vectors close
to the question vector. This project uses its flat L2 index.

### Q14. What does L2 distance mean here?

**Answer:** It measures distance between two vectors. A smaller value means
closer vectors for this search. It is not a percentage or probability.

### Q15. What is the role of Sentence Transformers?

**Answer:** It converts document chunks and user questions into embeddings so
they can be compared by meaning.

### Q16. What is the role of Groq?

**Answer:** The app sends the prompt to a language model through Groq's API and
uses the returned text as the answer.

### Q17. Where are files stored?

**Answer:** Uploaded PDFs are in `data/raw`. The FAISS index and pickled chunk
documents are in `storage`. Settings are also saved locally under storage.

### Q18. Does the system reprocess every PDF for every question?

**Answer:** No. It builds and saves the index first. Normal questions reuse the
saved index. If PDFs or indexing settings change, the user should rebuild it.

### Q19. How does chat history help?

**Answer:** If there is history, the pipeline asks the LLM to rewrite a
follow-up question as a standalone search question. The final prompt also
includes recent conversation messages.

### Q20. Where is chat history stored?

**Answer:** In Streamlit session state while the app session is active. The
project does not store it in a permanent chat database.

### Q21. How are page numbers shown correctly?

**Answer:** PDF page metadata is zero-based in the loaded documents. The prompt
and citation metadata add one so the user sees page numbers starting at one.

### Q22. Are the citations guaranteed proof for every sentence?

**Answer:** No. The app displays the retrieved chunks and their page details.
It does not verify a separate citation for every claim in the generated answer.

### Q23. What is temperature?

**Answer:** It controls how varied the generated text can be. A lower value
usually makes responses less varied; this project's default is zero.

### Q24. What happens when a PDF is deleted?

**Answer:** The document manager deletes the file and invalidates the saved
index, because the old index would still contain the deleted document's chunks.

### Q25. How do you evaluate the project?

**Answer:** The evaluation module runs a benchmark of questions and expected
answers. It reports answer correctness, context alignment, an overall score,
response time, and which metric backend was used.

### Q26. Does the evaluation always use RAGAS?

**Answer:** No. It tries RAGAS first. If RAGAS is unavailable or fails, the code
uses simple local word-overlap metrics.

### Q27. What is the biggest limitation?

**Answer:** Retrieval and LLM answers are not perfect. The system can miss
relevant text or misunderstand it, so users should check the displayed sources.
Scanned PDFs also need OCR support that is not part of the current loader.

### Q28. Is this fully local?

**Answer:** No. PDF processing, embeddings, and FAISS indexing are handled by
the application, but answer generation uses Groq's hosted API and needs a
network connection and API key.

### Q29. Why keep the API key out of the source code?

**Answer:** A key in source code can be accidentally shared. Reading it from an
environment variable keeps the secret separate from the code.

### Q30. What happens if the index files are missing?

**Answer:** The frontend does not load the RAG service until both the FAISS
index and document data files exist. The user needs to build the knowledge
base before asking document questions.

### Q31. What would happen with a very large collection?

**Answer:** The current flat index checks vectors directly and is simple to use.
For a much larger collection I would measure performance and consider an
approximate FAISS index or a dedicated vector database.

### Q32. What would you improve?

**Answer:** I would improve OCR, testing, evaluation data, sentence-level source
verification, and support for larger collections. I would also add persistent
user/chat management for a multi-user deployment.

## 17. Quick definitions to memorize

- **RAG:** Search first, generate an answer from the search results.
- **Embedding:** Numbers representing the meaning of text.
- **Chunk:** A smaller section of a document.
- **Overlap:** Repeated text between chunks to keep boundary context.
- **FAISS:** A library used here to search vectors.
- **Top-k:** Number of nearest chunks to return.
- **LLM:** The model that generates the final natural-language answer.
- **Grounded answer:** An answer intended to use supplied source text.
- **Metadata:** Information such as source filename and page number.
- **Evaluation benchmark:** Questions and expected answers used to measure
  system behavior.

## 18. Final 20-second answer

> This is a PDF question-answering app built with Streamlit and RAG. It extracts
> and chunks PDF text, embeds each chunk, and stores the vectors in FAISS. For a
> question, it retrieves the closest chunks and sends only those with the
> question to a Groq-hosted LLM. It shows the answer and source page details.
> This is more practical than sending a whole long PDF every time, but the
> retrieved evidence and generated answer still need to be checked.
