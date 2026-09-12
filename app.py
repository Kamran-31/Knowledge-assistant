"""
Knowledge Assistant - a NotebookLM-inspired RAG app.

Upload a PDF, Word, Excel, CSV, TXT, or image file and ask questions
about it. Answers are generated strictly from the uploaded content using
Retrieval-Augmented Generation.
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

# Base styles + targeted layout fixes
ENHANCED_CSS = f"""
{CUSTOM_CSS}

/* Bottom centered footer */
.app-footer {{
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border-top: 1px solid #e5e7eb;
    text-align: center;
    padding: 8px 16px;
    font-size: 0.78rem;
    color: #6b7280;
    z-index: 999;
    letter-spacing: 0.01em;
}}

/* Padding at bottom of page to prevent overlap with sticky footer */
.block-container {{
    padding-bottom: 3.5rem !important;
    padding-top: 2rem !important;
}}

/* Studio Action Buttons sizing and text visibility */
.studio-grid div[data-testid="stButton"] button {{
    min-height: 52px !important;
    height: auto !important;
    padding: 8px 10px !important;
    font-size: 0.84rem !important;
    line-height: 1.25 !important;
    white-space: normal !important;
    word-break: normal !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    border-radius: 8px !important;
    border: 1px solid #e5e7eb !important;
    background-color: #f9fafb !important;
    transition: all 0.15s ease-in-out !important;
}}

.studio-grid div[data-testid="stButton"] button:hover {{
    border-color: #2563eb !important;
    background-color: #eff6ff !important;
    color: #1d4ed8 !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
}}
"""
st.markdown(ENHANCED_CSS, unsafe_allow_html=True)


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
header_container = st.container()
with header_container:
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
                        <span style="font-size: 0.7rem; font-weight: 600; background: #e0e7ff; color: #4338ca; padding: 2px 7px; border-radius: 9999px; letter-spacing: 0.05em;">
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
            if st.button("＋ New", use_container_width=True, help="Create a clean session"):
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
                    help="Set if GROQ_API_KEY is not configured in secrets.",
                    label_visibility="collapsed",
                )
                st.session_state["manual_api_key"] = manual_key
                st.caption("Model: `openai/gpt-oss-20b`")

st.markdown("<div style='margin-top: 8px; margin-bottom: 12px; border-bottom: 1px solid #f0f2f5;'></div>", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# Main Grid Layout
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
                    f"<div class='history-item' style='display:flex; justify-content:space-between; margin-bottom:6px; font-size:0.86rem;'>"
                    f"<span>📄 {s.name}</span>"
                    f"<span style='color:#6b7280;'>{s.num_chunks} chunks</span>"
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
                    f"<div class='history-item' style='display:flex; justify-content:space-between; margin-bottom:5px; font-size:0.83rem;'>"
                    f"<span>📝 {item['title']}</span>"
                    f"<span style='color:#9ca3af;'>{item['time']}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            if len(st.session_state.notebook_sessions) > 8:
                st.button("Load more", use_container_width=True)

# --------------------------------------------------------------------------
# CENTER COLUMN — Chat / Canvas
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
                        Upload documentation, spreadsheets, or slides on the left. Ask questions to extract facts or generate outlines.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            col_hint1, col_hint2 = st.columns(2)
            with col_hint1:
                if st.button("💡 Summarize key takeaways", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": "Summarize the key takeaways of this material."})
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
        question = st.chat_input("Ask a question or request a synthesis...")
    with count_col:
        n = len(st.session_state.pipeline.sources)
        st.markdown(
            f"<div style='text-align:center; padding:6px; font-size:0.8rem; background:#f3f4f6; border-radius:6px; color:#4b5563; font-weight:500;'>"
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
# RIGHT COLUMN — Studio tools & Notes
# --------------------------------------------------------------------------
with right_col:
    with st.container(border=True):
        st.subheader("🎛️ Studio", anchor=False)

        tiles = [
            ("🔊 Audio Overview", "Audio Overview"),
            ("🖼️ Slide Deck", "Slide Deck"),
            ("🎬 Video Script", "Video Overview"),
            ("🧠 Mind Map", "Mind Map"),
            ("📊 Report Doc", "Reports"),
            ("🗂️ Flashcards", "Flashcards"),
            ("❓ Practice Quiz", "Quiz"),
            ("📈 Infographic", "Infographic"),
            ("📋 Data Table", "Data Table"),
        ]

        # Wrapped inside class container for responsive CSS sizing
        st.markdown('<div class="studio-grid">', unsafe_allow_html=True)
        t_col1, t_col2 = st.columns(2)
        for i, (label, key_name) in enumerate(tiles):
            target_col = t_col1 if i % 2 == 0 else t_col2
            with target_col:
                if st.button(label, key=f"studio_btn_{key_name}", use_container_width=True):
                    if not st.session_state.pipeline.has_sources():
                        st.warning("Upload a source first.")
                    else:
                        st.session_state.active_studio_tool = key_name
                        prompt_map = {
                            "Audio Overview": "Create an engaging two-person conversational podcast script summarizing the main takeaways from this document.",
                            "Slide Deck": "Generate a slide-by-slide outline (Title, Bullet Points, Speaker Notes) for a presentation based on this document.",
                            "Video Overview": "Draft a short 2-minute video script explaining the core insights of this document.",
                            "Mind Map": "Structure a hierarchical outline showing main themes and subtopics suitable for generating a mind map.",
                            "Reports": "Draft an executive briefing report detailing background, findings, and recommendations from this document.",
                            "Flashcards": "Create 5 study flashcards with 'Front: [Question]' and 'Back: [Answer]' based on this document.",
                            "Quiz": "Generate a 5-question multiple choice quiz with answer keys based on this material.",
                            "Infographic": "Outline the narrative structure and numerical data points needed to build an infographic about this topic.",
                            "Data Table": "Extract structured data, comparisons, and tabular facts into clean Markdown tables.",
                        }
                        user_request = prompt_map.get(key_name, f"Generate {key_name} content.")
                        st.session_state.chat_history.append({"role": "user", "content": user_request})

                        api_key = get_api_key()
                        if api_key:
                            with st.spinner(f"Creating {key_name}..."):
                                results = st.session_state.pipeline.retrieve(user_request, top_k=TOP_K)
                                context = st.session_state.pipeline.build_context(results)
                                try:
                                    res_text = generate_answer(user_request, context, api_key)
                                    used_sources = sorted({c.source for c, _ in results})
                                    st.session_state.chat_history.append(
                                        {"role": "assistant", "content": res_text, "sources": used_sources}
                                    )
                                except Exception as err:
                                    st.session_state.chat_history.append(
                                        {"role": "assistant", "content": f"Studio generation failed: {err}"}
                                    )
                        st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.subheader("📝 Workspace Notes", anchor=False)
        if not st.session_state.studio_notes:
            st.markdown(
                "<div style='text-align:center; padding:16px 8px; color:#9ca3af; font-size:0.83rem; line-height:1.4;'>"
                "Pinned summaries and custom scratch notes appear here."
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            for idx, note in enumerate(st.session_state.studio_notes):
                st.text_area(f"Note {idx+1}", note, height=80, key=f"note_area_{idx}")

        with st.popover("＋ Add note", use_container_width=True):
            new_note_val = st.text_area("Note content", placeholder="Paste or type notes...")
            if st.button("Save Note", use_container_width=True):
                if new_note_val.strip():
                    st.session_state.studio_notes.append(new_note_val.strip())
                    st.rerun()

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
