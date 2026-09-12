"""
A small in-memory FAISS index plus a parallel list of metadata (the chunk
text + which source file it came from). Since embeddings are normalized,
a flat inner-product index behaves like cosine similarity search.
"""

from __future__ import annotations

import faiss
import numpy as np

from modules.text_chunker import Chunk


class VectorStore:
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.chunks: list[Chunk] = []

    def add(self, vectors: np.ndarray, chunks: list[Chunk]) -> None:
        if len(vectors) == 0:
            return
        self.index.add(vectors)
        self.chunks.extend(chunks)

    def search(self, query_vector: np.ndarray, top_k: int) -> list[tuple[Chunk, float]]:
        if self.index.ntotal == 0:
            return []
        top_k = min(top_k, self.index.ntotal)
        query_vector = np.expand_dims(query_vector, axis=0)
        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append((self.chunks[idx], float(score)))
        return results

    @property
    def is_empty(self) -> bool:
        return self.index.ntotal == 0

    @property
    def num_chunks(self) -> int:
        return self.index.ntotal
