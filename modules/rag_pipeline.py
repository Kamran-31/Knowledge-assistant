"""
Ties together: file parsing -> chunking -> embedding -> FAISS indexing ->
retrieval -> Groq generation. This is the single object the UI layer
talks to.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from config import (
    CHUNK_OVERLAP_WORDS,
    CHUNK_SIZE_WORDS,
    MAX_CONTEXT_CHARS,
    TOP_K,
)
from modules.embeddings import embed_query, embed_texts
from modules.file_parsers import extract_text
from modules.text_chunker import Chunk, chunk_text
from modules.vector_store import VectorStore


@dataclass
class SourceFile:
    name: str
    num_chunks: int
    char_count: int


@dataclass
class RAGPipeline:
    vector_store: VectorStore | None = None
    sources: list[SourceFile] = field(default_factory=list)

    def add_document(self, filename: str, file_bytes: bytes) -> SourceFile:
        raw_text = extract_text(filename, file_bytes)
        raw_text = raw_text.strip()

        if not raw_text:
            raise ValueError(
                f"No readable text could be extracted from '{filename}'. "
                "If it's a scanned image or image-only PDF, make sure the text is legible."
            )

        chunks: list[Chunk] = chunk_text(
            raw_text, source=filename, chunk_size=CHUNK_SIZE_WORDS, overlap=CHUNK_OVERLAP_WORDS
        )

        vectors = embed_texts([c.text for c in chunks])

        if self.vector_store is None:
            self.vector_store = VectorStore(dimension=vectors.shape[1])

        self.vector_store.add(vectors, chunks)

        source = SourceFile(name=filename, num_chunks=len(chunks), char_count=len(raw_text))
        self.sources.append(source)
        return source

    def has_sources(self) -> bool:
        return self.vector_store is not None and not self.vector_store.is_empty

    def retrieve(self, question: str, top_k: int = TOP_K) -> list[tuple[Chunk, float]]:
        if not self.has_sources():
            return []
        query_vector = embed_query(question)
        return self.vector_store.search(query_vector, top_k=top_k)

    @staticmethod
    def build_context(results: list[tuple[Chunk, float]]) -> str:
        pieces = []
        total_len = 0
        for chunk, score in results:
            piece = f"[Source: {chunk.source}]\n{chunk.text}"
            if total_len + len(piece) > MAX_CONTEXT_CHARS:
                break
            pieces.append(piece)
            total_len += len(piece)
        return "\n\n---\n\n".join(pieces)
