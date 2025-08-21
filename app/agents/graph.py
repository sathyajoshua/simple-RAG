from langgraph.graph import StateGraph, START, END
from typing import Dict
from app.rag.retriever import retrieve as rag_retrieve
import os
from openai import OpenAI
import logging
logging.basicConfig(level=logging.INFO)

def needs_retrieval(state):
    q = state["query"].lower()
    state["do_retrieve"] = any(
        k in q for k in ["report","trend","earnings","revenue","price","table","risk","compare"]
    )
    return state

def retrieval_node(state):
    logging.info(f"Retrieval node received state: {state}")
    ctx = rag_retrieve(state["query"], k=5)
    state["context"] = ctx
    return state

def generate_node(state):
    print("DEBUG: OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))
    ctx = state.get("context", [])
    prompt = f"You are an investment assistant. Use the context to answer.\n\nQuestion: {state['query']}\n\nContext:\n"
    for text, meta in ctx:
        prompt += f"- {text[:500]}\n"
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    state["answer"] = resp.choices[0].message.content
    state["sources"] = [{"source": m["source"], "page": m.get("page")} for _, m in ctx][:3]
    return state

def build_graph():
    g = StateGraph(dict)

    # Nodes
    g.add_node("route", needs_retrieval)
    g.add_node("retrieve", retrieval_node)
    g.add_node("generate", generate_node)

    # Flow
    g.add_conditional_edges(
        "route",
        lambda s: "retrieve" if s.get("do_retrieve", True) else "generate",
        {"retrieve": "retrieve", "generate": "generate"},
    )

    g.add_edge("retrieve", "generate")
    g.add_edge("generate", END)
    g.add_edge(START, "route")

    return g.compile()
