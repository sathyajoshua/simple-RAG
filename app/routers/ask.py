from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from app.core.config import settings
from app.agents.graph import build_graph

router = APIRouter()
graph = build_graph()

class AskIn(BaseModel):
    query: str

def check_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

@router.post("/", dependencies=[Depends(check_api_key)])
def ask(payload: AskIn):
    state = {"query": payload.query}
    out = graph.invoke(state)
    print("Graph output:", out)
    return {"answer": out.get("answer",""), "sources": out.get("sources",[])}
