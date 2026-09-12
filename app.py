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
        "chat_history": [],
        "notebook_title": DEFAULT_NOTEBOOK_TITLE,
        "notebook_sessions": [],
        "processed_files": set(),
        "active_studio_tool": None,
        "studio_notes": [],
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
header_col1, header_col2 = st.columns([2.5, 2.5], vertical_alignment="center")

with header_col1:
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 12px; padding: 4px 0;">
            <div style="display: flex; align-items: center; justify-content: center; width: 34px; height: 34px; border-radius: 8px; background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; font-size: 16px; box-shadow: 0 2px 4px rgba(37,99,235,0.2);">
                ◈
            </div>
            <div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.15rem; font-weight: 700; color: #111827; letter-spacing: -0.01em;">
                        {st.session_state.notebook_title}
                    </span>
                    <span style="font-size: 0.7rem; font-weight: 600; background: #e0e7ff; color: #4338ca; padding: 2px 7px; border-radius: 9999px;">
                        STUDIO
                    </span>
                </div>
                <div style="font-size: 0.78rem; color: #6b7280; display: flex; gap: 8px;">
                    <span>Knowledge Base</span>
                    <span>•</span>
                    <span>Multi-modal RAG</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_col2:
    hc1, hc2, hc3, hc4 = st.columns([1.2, 0.9, 0.9, 1.1], gap="small")
    with hc1:
        if st.button("＋ New", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.notebook_title = DEFAULT_NOTEBOOK_TITLE
            st.rerun()
    with hc2:
        st.button("📋 Copy", use_container_width=True)
    with hc3:
        st.button("🔗 Share", use_container_width=True)
    with hc4:
        with st.popover("⚙️ Settings", use_container_width=True):
            st.caption("Groq API key")
            manual_key = st.text_input(
                "GROQ_API_KEY",
                type="password",
                value=st.session_state.get("manual_api_key", ""),
                help="Set if not already in Streamlit secrets.",
                label_visibility="collapsed",
            )
            st.session_state["manual_api_key"] = manual_key
            st.caption("Model: `openai/gpt-oss-20b`")

st.markdown("<div style='margin-top: 6px; margin-bottom: 12px; border-bottom: 1px solid #ECEAE4;'></div>", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# Main Columns
# --------------------------------------------------------------------------
left_col, center_col, right_col = st.columns([1.1, 2.2, 1.2], gap="medium")

# --------------------------------------------------------------------------
# LEFT COLUMN — Sources + Notebook history
# --------------------------------------------------------------------------
with left_col:
    with st.container(border=True):
        st.subheader("📁 Sources", anchor=False)
        st.caption(f"Accepted: {SUPPORTED_EXTENSIONS_LABEL}")

        uploaded_files = st.file_uploader(
            "Upload files",
            type=SUPPORTED_EXTENSIONS,
            accept_multiple_files=True,
            label_visibility="collapsed",
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
            st.divider()
            for s in st.session_state.pipeline.sources:
                st.markdown(
                    f"<div class='history-item'>"
                    f"<span>📄 {s.name}</span>"
                    f"<span style='color:#6b7280; font-size:0.78rem;'>{s.num_chunks} chunks</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

    with st.container(border=True):
        st.subheader("🕓 Session History", anchor=False)
        if not st.session_state.notebook_sessions:
            st.caption("Indexed files for this run will appear here.")
        else:
            for item in st.session_state.notebook_sessions[:8]:
                st.markdown(
                    f"<div class='history-item'>"
                    f"<span>📝 {item['title']}</span>"
                    f"<span style='color:#9ca3af; font-size:0.75rem;'>{item['time']}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            if len(st.session_state.notebook_sessions) > 8:
                st.button("Load more", use_container_width=True)

# --------------------------------------------------------------------------
# CENTER COLUMN — Chat Canvas
# --------------------------------------------------------------------------
with center_col:
    chat_container = st.container(height=580, border=True)

    with chat_container:
        if not st.session_state.chat_history:
            st.markdown(
                """
                <div style="text-align: center; padding: 45px 16px;">
                    <div style="font-size: 2.3rem; margin-bottom: 12px;">👋</div>
                    <h3 style="margin-bottom: 6px; font-weight: 600;">Welcome to your Knowledge Assistant</h3>
                    <p style="color: #6b7280; font-size: 0.92rem; max-width: 460px; margin: 0 auto 18px auto; line-height: 1.5;">
                        Upload documentation or spreadsheets on the left. Ask questions to extract facts or generate structured reports.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            col_hint1, col_hint2 = st.columns(2)
            with col_hint1:
                if st.button("💡 Key takeaways", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": "Summarize key takeaways."})
                    st.rerun()
            with col_hint2:
                if st.button("📝 Executive briefing", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": "Provide a high-level executive briefing."})
                    st.rerun()
        else:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
                    if msg.get("sources"):
                        with st.expander("Sources cited"):
                            for s in msg["sources"]:
                                st.caption(f"• {s}")

    input_col, count_col = st.columns([5, 1], vertical_alignment="center")
    with input_col:
        question = st.chat_input("Ask a question or request an outline...")
    with count_col:
        n = len(st.session_state.pipeline.sources)
        st.markdown(
            f"<div style='text-align:center; padding:6px; font-size:0.8rem; background:#EFEFEA; border-radius:8px; color:#4B5563; font-weight:600;'>"
            f"{n} source{'s' if n != 1 else ''}</div>",
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
            answer = "No Groq API key found. Add one in **⚙️ Settings** (top right) or set `GROQ_API_KEY`."
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.rerun()

        with st.spinner("Analyzing context..."):
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
# RIGHT COLUMN — Interactive Studio Tools & Notes
# --------------------------------------------------------------------------
# RIGHT COLUMN — Interactive Studio Tools & Notes
with right_col:
    with st.container(border=True):
        st.subheader("🎛️ Studio", anchor=False)

        tiles = [
            ("🔊\nAudio Overview", "Audio Overview"),
            ("🖼️\nSlide Deck", "Slide Deck"),
            ("🎬\nVideo Script", "Video Overview"),
            ("🧠\nMind Map", "Mind Map"),
            ("📊\nReport Doc", "Reports"),
            ("🗂️\nFlashcards", "Flashcards"),
            ("❓\nPractice Quiz", "Quiz"),
            ("📈\nInfographic", "Infographic"),
            ("📋\nData Table", "Data Table"),
        ]

        # Use an outer wrapper so CSS can directly target these buttons without nth-child guessing
        st.markdown('<div class="studio-card">', unsafe_allow_html=True)
        t_col1, t_col2 = st.columns(2)
        for i, (label, key_name) in enumerate(tiles):
            target_col = t_col1 if (i % 2 == 0) else t_col2
            with target_col:
                if st.button(label, key=f"btn_{key_name}", use_container_width=True):
                    if not st.session_state.pipeline.has_sources():
                        # Use toast instead of st.warning so it does NOT push column elements out of grid alignment
                        st.toast("⚠️ Please upload at least one source first!", icon="📁")
                    else:
                        prompt_map = {
                            "Audio Overview": "Create an engaging two-person conversational podcast script summarizing the main takeaways from this document.",
                            "Slide Deck": "Generate a slide-by-slide outline (Title, Bullet Points, Speaker Notes) for a presentation based on this document.",
                            "Video Overview": "Draft a short 2-minute video script explaining the core insights of this document.",
                            "Mind Map": "Structure a hierarchical outline showing main themes and subtopics suitable for generating a mind map.",
                            "Reports": "Draft an executive briefing report detailing background, findings, and recommendations from this document.",
                            "Flashcards": "Create 5 study flashcards with 'Front: [Question]' and 'Back: [Answer]' based on this document.",
                            "Quiz": "Generate a 5-question multiple choice quiz with answer keys based on this material.",
                            "Infographic": "Outline the narrative structure and numerical data points needed to build an infographic about this topic.",
                            "Data Table": "Extract structured data, comparisons, and tabular facts into Markdown tables.",
                        }
                        req = prompt_map.get(key_name, f"Generate {key_name} content.")
                        st.session_state.chat_history.append({"role": "user", "content": req})

                        api_key = get_api_key()
                        if api_key:
                            with st.spinner(f"Generating {key_name}..."):
                                results = st.session_state.pipeline.retrieve(req, top_k=TOP_K)
                                context = st.session_state.pipeline.build_context(results)
                                try:
                                    out_text = generate_answer(req, context, api_key)
                                    used_sources = sorted({c.source for c, _ in results})
                                    st.session_state.chat_history.append(
                                        {"role": "assistant", "content": out_text, "sources": used_sources}
                                    )
                                except Exception as err:
                                    st.session_state.chat_history.append(
                                        {"role": "assistant", "content": f"Error: {err}"}
                                    )
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------------------------------
# Bottom Centered Fixed Footer
# --------------------------------------------------------------------------
st.markdown(
    """
    <div class="app-footer">
        Knowledge Assistant · RAG powered by sentence-transformers + FAISS + Groq (openai/gpt-oss-20b)
    </div>
    """,
    unsafe_allow_html=True,
)
