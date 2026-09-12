"""
Splits long text into overlapping, word-based chunks that get embedded
and indexed individually. Overlap helps preserve context across chunk
boundaries so answers don't get cut off mid-idea.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    source: str
    chunk_id: int


def chunk_text(text: str, source: str, chunk_size: int, overlap: int) -> list[Chunk]:
    words = text.split()
    if not words:
        return []

    chunks: list[Chunk] = []
    start = 0
    chunk_id = 0
    step = max(chunk_size - overlap, 1)

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_str = " ".join(chunk_words).strip()
        if chunk_str:
            chunks.append(Chunk(text=chunk_str, source=source, chunk_id=chunk_id))
            chunk_id += 1
        start += step

    return chunks
