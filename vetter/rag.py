from pathlib import Path

import faiss
import numpy as np
import ollama

EMBED_MODEL = "nomic-embed-text"
DOCS_DIR = Path(__file__).parent.parent / "docs"


def embed(texts):
    response = ollama.embed(model=EMBED_MODEL, input=texts)
    vectors = np.array(response["embeddings"], dtype="float32")
    faiss.normalize_L2(vectors)
    return vectors


def build_index():
    paths = sorted(p for p in DOCS_DIR.glob("*.md") if p.name != "README.md")
    notes = [{"source": p.name, "text": p.read_text(encoding="utf-8")} for p in paths]
    vectors = embed([note["text"] for note in notes])
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)
    return index, notes


def search(index, notes, query, k=1):
    scores, positions = index.search(embed([query]), k)
    return [notes[i] for i in positions[0]]