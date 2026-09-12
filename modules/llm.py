"""
Handles all communication with Groq's chat completion endpoint
(model: openai/gpt-oss-20b). The system prompt strictly constrains the
model to answer only from the retrieved document context, regardless of
what subject/field the uploaded file belongs to.
"""

from __future__ import annotations

import streamlit as st
from groq import Groq

from config import GROQ_MODEL_NAME, LLM_MAX_TOKENS, LLM_TEMPERATURE

SYSTEM_PROMPT = """You are a careful research assistant embedded in a notebook app.
You must answer the user's question using ONLY the "CONTEXT" excerpts provided below,
which were retrieved from document(s) the user uploaded. The document can be about
absolutely any topic or field (business, science, legal, medical, personal, technical, etc.) -
treat all subject matter neutrally and answer factually from the context.

Rules:
- Base your answer strictly on the provided context. Do not use outside knowledge to add
  facts that are not supported by the context.
- If the context does not contain enough information to answer, clearly say so instead of
  guessing: "I couldn't find that information in the uploaded document(s)."
- When helpful, mention which source file / page / sheet the information came from.
- Be concise, clear, and well-structured. Use bullet points or short paragraphs where useful.
- Never invent citations, numbers, or facts that are not present in the context.
"""


@st.cache_resource(show_spinner=False)
def _get_client(api_key: str) -> Groq:
    return Groq(api_key=api_key)


def generate_answer(question: str, context: str, api_key: str) -> str:
    client = _get_client(api_key)

    user_prompt = f"""CONTEXT:
{context}

QUESTION:
{question}

Answer the question using only the context above."""

    response = client.chat.completions.create(
        model=GROQ_MODEL_NAME,
        temperature=LLM_TEMPERATURE,
        max_tokens=LLM_MAX_TOKENS,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content.strip()
