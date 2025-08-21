import os
from chromadb import Client
from chromadb.config import Settings

_client = None
_collection = None

def get_chroma_collection(name="docs"):
    global _client, _collection
    if _client is None:
        _client = Client(Settings(persist_directory="data/processed/chroma"))
    if _collection is None:
        _collection = _client.get_or_create_collection(name=name)
    return _collection
