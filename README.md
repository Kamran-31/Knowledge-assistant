# 📘 Knowledge Assistant — RAG-powered Notebook

A NotebookLM-inspired AI research assistant. Upload a document — from any
field of life (business, legal, medical, academic, personal, technical,
etc.) — and ask questions about it. Answers are generated **only from the
content of your uploaded files** using Retrieval-Augmented Generation (RAG).

## ✨ Features

- **Multi-format ingestion**: PDF, Word (`.docx`), Excel (`.xlsx` / `.xls`),
  CSV, TXT, and images (`.jpg` / `.png`, via OCR).
- **Semantic search**: `fastembed` (ONNX, no PyTorch) embeddings + `FAISS` vector index.
- **Grounded answers**: `Groq` (`openai/gpt-oss-20b`) generates answers strictly
  from retrieved context, with source attribution.
- **Modern, modular UI**: three-column NotebookLM-style layout (Sources &
  History / Chat / Studio) built with Streamlit + custom CSS.
- **Clean, scalable codebase**: parsing, chunking, embeddings, vector store,
  LLM calls, and UI are all separated into their own modules.

## 🧠 How it works (RAG pipeline)

1. **Upload** a file → `file_parsers.py` extracts raw text (OCR for images).
2. **Chunk** the text into overlapping ~220-word pieces (`text_chunker.py`).
3. **Embed** each chunk with `all-MiniLM-L6-v2` (`embeddings.py`).
4. **Index** the vectors in a FAISS `IndexFlatIP` store (`vector_store.py`).
5. **Ask a question** → the question is embedded and the top-K most similar
   chunks are retrieved.
6. **Generate** → retrieved chunks are passed as context to Groq's
   `openai/gpt-oss-20b` model, which is instructed to answer *only* from
   that context.

## 🚀 Run locally

### 1. Clone and set up a virtual environment

```bash
git clone https://github.com/<Kamran-31>/knowledge-assistant.git
cd knowledge-assistant
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 2. Install system dependency for OCR (Tesseract)

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Groq API key

Get a free key at [console.groq.com](https://console.groq.com/keys), then:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "gsk_your_real_key_here"
```

(Alternatively, paste the key into the **⚙️ Settings** popover inside the
running app — useful for quick testing without touching secrets.)

### 5. Run the app

```bash
streamlit run app.py
```

Open the local URL Streamlit prints (usually `http://localhost:8501`).

## 🛡️ Notes & limitations

- Answers are grounded strictly in uploaded content — if the document
  doesn't contain the answer, the assistant says so instead of guessing.
- Image OCR quality depends on image clarity; scanned/handwritten text may
  extract poorly.
- The in-app "Notebook History" and "Studio" tools reflect the current
  browser session only (no database is wired up) — everything resets on
  a full app restart. Swap in a persistent store (SQLite/Postgres/S3) if
  you need durability across sessions.
- Vector index is in-memory per session; very large documents will use
  more RAM — trim `CHUNK_SIZE_WORDS`/file size if you hit Streamlit
  Cloud's free-tier memory limits.


