"""
Lightweight embedding wrapper using fastembed (ONNX runtime based).
No PyTorch dependency -> much smaller install footprint and far more
reliable to build on memory-constrained hosts like Streamlit Community
Cloud's free tier.
"""

from __future__ import annotations

import numpy as np
import streamlit as st
from fastembed import TextEmbedding

from config import EMBEDDING_MODEL_NAME


@st.cache_resource(show_spinner="Loading embedding model...")
def load_embedding_model() -> TextEmbedding:
    return TextEmbedding(model_name=EMBEDDING_MODEL_NAME)


def _normalize(vectors: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1e-8
    return vectors / norms


def embed_texts(texts: list[str]) -> np.ndarray:
    model = load_embedding_model()
    vectors = np.array(list(model.embed(texts)), dtype="float32")
    return _normalize(vectors).astype("float32")


def embed_query(query: str) -> np.ndarray:
    return embed_texts([query])[0]
