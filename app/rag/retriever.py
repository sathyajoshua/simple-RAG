from app.rag.vectorstore import get_chroma_collection
from app.rag.embedder import embed_texts

def add_docs(docs, batch_size=5000):
    col = get_chroma_collection()
    for i in range(0, len(docs), batch_size):
        batch = docs[i:i+batch_size]
        embeddings = embed_texts([d["text"] for d in batch])
        col.add(
            documents=[d["text"] for d in batch],
            metadatas=[d["meta"] for d in batch],
            ids=[d["id"] for d in batch],
            embeddings=embeddings
        )

def retrieve(query: str, k: int = 5):
    col = get_chroma_collection()
    q_emb = embed_texts([query])[0]
    res = col.query(query_embeddings=[q_emb], n_results=k)
    # return (text, meta) pairs
    return list(zip(res["documents"][0], res["metadatas"][0]))
