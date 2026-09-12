"""
Knowledge Assistant - a NotebookLM-inspired RAG app.

Upload a PDF, Word, Excel, CSV, TXT, or image file and ask questions
about it. Answers are generated strictly from the uploaded content using
Retrieval-Augmented Generation:

    sentence-transformers (embeddings) -> FAISS (vector search)
    -> Groq / openai-gpt-oss-20b (answer generation)

Run locally:  streamlit run app.py
"""

from __future__ import annotations

import datetime as dt
import os

import streamlit as st

from config import (
    APP_NAME,
    DEFAULT_NOTEBOOK_TITLE,
    GROQ_API_KEY_ENV,
    SUPPORTED_EXTENSIONS,
    SUPPORTED_EXTENSIONS_LABEL,
    TOP_K,
)
from modules.llm import generate_answer
from modules.rag_pipeline import RAGPipeline
from modules.ui_styles import CUSTOM_CSS

st.set_page_config(page_title=f"{APP_NAME}", page_icon="🔵", layout="wide")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------
def init_state():
    defaults = {
        "pipeline": RAGPipeline(),
        "chat_history": [],  # list of {"role": ..., "content": ...}
        "notebook_title": DEFAULT_NOTEBOOK_TITLE,
        "notebook_sessions": [],  # simple in-memory "history" of notebooks this run
        "processed_files": set(),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


def get_api_key() -> str | None:
    key = os.environ.get(GROQ_API_KEY_ENV)
    if not key:
        try:
            key = st.secrets.get(GROQ_API_KEY_ENV)
        except Exception:
            key = None
    return key or st.session_state.get("manual_api_key")


# --------------------------------------------------------------------------
# Header bar
# --------------------------------------------------------------------------
header_col1, header_col2 = st.columns([3, 4])
with header_col1:
    st.markdown(
        f"""
        <div class="notebook-header" style="margin-bottom:0;">
            <div class="brand">
                <span class="logo-dot"></span>
                {st.session_state.notebook_title}
                <span class="pro-badge">PRO</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with header_col2:
    hc1, hc2, hc3, hc4, hc5 = st.columns(5)
    with hc1:
        st.button("＋ Create notebook", use_container_width=True)
    with hc2:
        st.button("Copy", use_container_width=True)
    with hc3:
        st.button("Analytics", use_container_width=True)
    with hc4:
        st.button("Share", use_container_width=True)
    with hc5:
        with st.popover("⚙️ Settings", use_container_width=True):
            st.caption("Groq API key")
            manual_key = st.text_input(
                "GROQ_API_KEY",
                type="password",
                value=st.session_state.get("manual_api_key", ""),
                help="Only needed if it isn't already set in Streamlit secrets.",
                label_visibility="collapsed",
            )
            st.session_state["manual_api_key"] = manual_key
            st.caption(f"Model: `openai/gpt-oss-20b` via Groq")

st.write("")

left_col, center_col, right_col = st.columns([1.1, 2.2, 1.1], gap="medium")

# --------------------------------------------------------------------------
# LEFT COLUMN — Sources + Notebook history
# --------------------------------------------------------------------------
with left_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h4>📁 Sources</h4>", unsafe_allow_html=True)
    st.caption(f"Supported: {SUPPORTED_EXTENSIONS_LABEL}")

    uploaded_files = st.file_uploader(
        "＋ Add sources",
        type=SUPPORTED_EXTENSIONS,
        accept_multiple_files=True,
        label_visibility="visible",
    )

    if uploaded_files:
        for uf in uploaded_files:
            file_key = f"{uf.name}-{uf.size}"
            if file_key in st.session_state.processed_files:
                continue
            with st.spinner(f"Indexing '{uf.name}'..."):
                try:
                    file_bytes = uf.read()
                    source = st.session_state.pipeline.add_document(uf.name, file_bytes)
                    st.session_state.processed_files.add(file_key)
                    st.session_state.notebook_sessions.insert(
                        0,
                        {
                            "title": uf.name,
                            "time": dt.datetime.now().strftime("%I:%M %p"),
                        },
                    )
                    st.success(f"Indexed '{uf.name}' ({source.num_chunks} chunks)")
                except Exception as e:
                    st.error(f"Could not process '{uf.name}': {e}")

    if st.session_state.pipeline.sources:
        st.markdown("<hr style='margin:0.6rem 0;border-color:#ECEAE4;'>", unsafe_allow_html=True)
        for s in st.session_state.pipeline.sources:
            st.markdown(
                f"<div class='history-item'>📄 {s.name}"
                f"<span class='history-time'>{s.num_chunks} chunks</span></div>",
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

    # ---- Notebook history card ----
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h4>🕓 Notebook History</h4>", unsafe_allow_html=True)

    if not st.session_state.notebook_sessions:
        st.markdown(
            "<span class='card-subtle'>Uploaded sources for this session will appear here.</span>",
            unsafe_allow_html=True,
        )
    else:
        for item in st.session_state.notebook_sessions[:8]:
            st.markdown(
                f"<div class='history-item'>📝 {item['title']}"
                f"<span class='history-time'>{item['time']}</span></div>",
                unsafe_allow_html=True,
            )
        if len(st.session_state.notebook_sessions) > 8:
            st.button("Load more", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# CENTER COLUMN — Chat / synthesis canvas
# --------------------------------------------------------------------------
with center_col:
    chat_container = st.container(height=560, border=True)

    with chat_container:
        if not st.session_state.chat_history:
            st.markdown(
                """
                <div class="welcome-wrap">
                    <div class="emoji">👋</div>
                    <h2>Let's start your notebook...</h2>
                    <p>Add a source on the left, then ask anything about it — the answers
                    come straight from your document, whatever field it's from.</p>
                    <div class="chip-row">
                        <span class="chip">Learn about a new topic</span>
                        <span class="chip">Create something new</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
                    if msg.get("sources"):
                        with st.expander("Sources used"):
                            for s in msg["sources"]:
                                st.caption(f"• {s}")

    st.write("")
    input_col, count_col = st.columns([5, 1])
    with input_col:
        question = st.chat_input("Ask a question or create something")
    with count_col:
        n = len(st.session_state.pipeline.sources)
        st.markdown(
            f"<div class='source-tag' style='margin-top:0.6rem;'>{n} source{'s' if n != 1 else ''}</div>",
            unsafe_allow_html=True,
        )

    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})

        if not st.session_state.pipeline.has_sources():
            answer = "Please add at least one source file on the left before asking a question."
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.rerun()

        api_key = get_api_key()
        if not api_key:
            answer = (
                "No Groq API key found. Add one in **⚙️ Settings** (top right) "
                "or set `GROQ_API_KEY` in Streamlit secrets."
            )
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.rerun()

        with st.spinner("Thinking..."):
            results = st.session_state.pipeline.retrieve(question, top_k=TOP_K)
            context = st.session_state.pipeline.build_context(results)
            try:
                answer = generate_answer(question, context, api_key)
            except Exception as e:
                answer = f"Something went wrong calling the model: {e}"

        used_sources = sorted({c.source for c, _ in results})
        st.session_state.chat_history.append(
            {"role": "assistant", "content": answer, "sources": used_sources}
        )
        st.rerun()

# --------------------------------------------------------------------------
# RIGHT COLUMN — Studio tools
# --------------------------------------------------------------------------
with right_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h4>🎛️ Studio</h4>", unsafe_allow_html=True)

    tiles = [
        ("🔊", "Audio Overview"),
        ("🖼️", "Slide Deck"),
        ("🎬", "Video Overview"),
        ("🧠", "Mind Map"),
        ("📊", "Reports"),
        ("🗂️", "Flashcards"),
        ("❓", "Quiz"),
        ("📈", "Infographic"),
        ("📋", "Data Table"),
    ]
    tile_cols = st.columns(2)
    for i, (icon, label) in enumerate(tiles):
        with tile_cols[i % 2]:
            st.markdown(
                f"<div class='studio-tile'>{icon} &nbsp; {label} &nbsp; ›</div>",
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        "<div class='studio-placeholder'>✏️<br>Studio output will be saved here</div>",
        unsafe_allow_html=True,
    )
    st.button("＋ Add note", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.caption(
    "Knowledge Assistant · RAG powered by sentence-transformers + FAISS + "
    "Groq (openai/gpt-oss-20b)"
)
