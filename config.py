"""
Central configuration for the Knowledge Assistant app.
Change models / chunking behaviour here without touching the rest of the code.
"""

import os

# ---- Branding ----
APP_NAME = "Notebook AI"
DEFAULT_NOTEBOOK_TITLE = "Untitled notebook"

# ---- Embeddings ----
# Small + fast ONNX model (via fastembed), no PyTorch dependency -
# reliable to install on Streamlit Community Cloud's free tier.
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"

# ---- LLM (Groq) ----
GROQ_MODEL_NAME = "openai/gpt-oss-20b"
GROQ_API_KEY_ENV = "GROQ_API_KEY"
LLM_TEMPERATURE = 0.2
LLM_MAX_TOKENS = 1024

# ---- Chunking ----
CHUNK_SIZE_WORDS = 220          # words per chunk
CHUNK_OVERLAP_WORDS = 40        # overlap between consecutive chunks

# ---- Retrieval ----
TOP_K = 5
MAX_CONTEXT_CHARS = 8000

# ---- Supported file types ----
SUPPORTED_EXTENSIONS = ["pdf", "docx", "xlsx", "xls", "csv", "txt", "jpg", "jpeg", "png"]

SUPPORTED_EXTENSIONS_LABEL = "PDF, Word (.docx), Excel (.xlsx/.xls), CSV, TXT, Images (.jpg/.png)"

# ---- Misc ----
MAX_FILE_SIZE_MB = 50
