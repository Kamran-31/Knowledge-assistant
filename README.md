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

## 🗂️ Project structure

```
knowledge-assistant/
├── app.py                      # Main Streamlit app (UI + orchestration)
├── config.py                   # All tunable constants (models, chunk size, etc.)
├── requirements.txt            # Python dependencies
├── packages.txt                # System (apt) dependencies — needed for OCR
├── README.md
├── .gitignore
├── .streamlit/
│   ├── config.toml             # Theme settings
│   └── secrets.toml.example    # Template for your API key (copy -> secrets.toml)
└── modules/
    ├── __init__.py
    ├── file_parsers.py         # Extracts text from pdf/docx/xlsx/csv/txt/images
    ├── text_chunker.py         # Splits text into overlapping chunks
    ├── embeddings.py           # fastembed (ONNX) wrapper
    ├── vector_store.py         # FAISS index wrapper
    ├── llm.py                  # Groq chat-completion wrapper
    ├── rag_pipeline.py         # Glues parsing -> chunking -> embedding -> retrieval
    └── ui_styles.py            # Custom CSS for the NotebookLM-style UI
```

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
git clone https://github.com/<your-username>/knowledge-assistant.git
cd knowledge-assistant
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 2. Install system dependency for OCR (Tesseract)

- **macOS**: `brew install tesseract`
- **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
- **Windows**: install from the
  [UB-Mannheim Tesseract build](https://github.com/UB-Mannheim/tesseract/wiki)
  and make sure `tesseract.exe` is on your PATH.

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

## ☁️ Deploy live on Streamlit Community Cloud — step by step

1. **Create a GitHub repository**
   - Go to [github.com/new](https://github.com/new), name it (e.g.
     `knowledge-assistant`), keep it public or private, and create it.

2. **Push these files to the repo**
   ```bash
   cd knowledge-assistant
   git init
   git add .
   git commit -m "Initial commit: RAG knowledge assistant"
   git branch -M main
   git remote add origin https://github.com/<your-username>/knowledge-assistant.git
   git push -u origin main
   ```
   > ⚠️ Do **not** commit a real `secrets.toml` file — it's already excluded
   > by `.gitignore`. Only `secrets.toml.example` (no real key) should be pushed.

3. **Create the app on Streamlit Community Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
   - Click **"Create app"** → **"From existing repo"**.
   - Select your repository, branch `main`, and main file path `app.py`.

4. **Add your secret**
   - In the app creation screen (or later via **⋮ → Settings → Secrets**),
     paste:
     ```toml
     GROQ_API_KEY = "gsk_your_real_key_here"
     ```

5. **Confirm `packages.txt` is picked up**
   - Streamlit Cloud automatically installs anything listed in
     `packages.txt` (here, `tesseract-ocr` for image OCR) via `apt-get`
     before installing Python requirements — no extra action needed as
     long as the file sits in the repo root.

6. **Deploy**
   - Click **"Deploy"**. The first build takes a few minutes (it downloads
     the embedding model and installs dependencies).
   - Your app will be live at:
     `https://<your-app-name>.streamlit.app`

7. **Redeploying after changes**
   - Just `git push` to `main` — Streamlit Cloud auto-redeploys.

## ⚙️ Configuration

All tunables live in `config.py`:

| Setting | Purpose |
|---|---|
| `EMBEDDING_MODEL_NAME` | fastembed (ONNX) model used for embeddings |
| `GROQ_MODEL_NAME` | Groq model used for answer generation |
| `CHUNK_SIZE_WORDS` / `CHUNK_OVERLAP_WORDS` | Text chunking behavior |
| `TOP_K` | How many chunks are retrieved per question |
| `MAX_CONTEXT_CHARS` | Cap on context length sent to the LLM |
| `SUPPORTED_EXTENSIONS` | File types accepted by the uploader |

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

## 📄 License

MIT — use freely, adapt as needed.
