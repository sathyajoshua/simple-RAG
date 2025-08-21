from fastapi import FastAPI
from app.core.logging import setup_logging
from app.core.instrumentation import setup_instrumentation
from app.routers import ask, ingest, health

setup_logging()
app = FastAPI(title="Investment Insights AI Backend", version="0.1.0")

setup_instrumentation(app)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(ingest.router, prefix="/ingest", tags=["ingest"])
app.include_router(ask.router, prefix="/ask", tags=["ask"])
