from fastapi import APIRouter, UploadFile, File
import fitz, uuid, pandas as pd
from app.rag.retriever import add_docs

router = APIRouter()

@router.post("/pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    doc = fitz.open(stream=await file.read(), filetype="pdf")
    chunks = []
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        if not text: continue
        chunks.append({"id": f"{uuid.uuid4()}",
                       "text": text[:4000],  # naive chunking
                       "meta": {"source": file.filename, "page": i+1}})
    add_docs(chunks)
    return {"ingested_pages": len(chunks)}

@router.post("/csv")
async def ingest_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    # turn rows into text snippets
    chunks = []
    for i, row in df.iterrows():
        txt = " | ".join([f"{c}:{row[c]}" for c in df.columns])[:4000]
        chunks.append({"id": f"{uuid.uuid4()}",
                       "text": txt,
                       "meta": {"source": file.filename, "row": int(i)}})
    add_docs(chunks)
    return {"ingested_rows": len(chunks)}
