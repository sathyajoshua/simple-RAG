import os
from sentence_transformers import SentenceTransformer
from typing import List

_model = None

def get_embedder():
    global _model
    if _model is None:
        name = os.getenv("EMBEDDINGS_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        _model = SentenceTransformer(name)
    return _model

def embed_texts(texts: List[str]):
    model = get_embedder()
    return model.encode(texts, show_progress_bar=False).tolist()
