from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# -----------------------------
# 1️⃣ Determine absolute path to your .env
# -----------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DOTENV_PATH = os.path.join(PROJECT_ROOT, ".env")

print("DEBUG: Loading .env from:", DOTENV_PATH)
load_dotenv(dotenv_path=DOTENV_PATH, override=True)

class Settings(BaseSettings):
    ENV: str = "dev"
    API_KEY: str = "changeme"
    VECTOR_BACKEND: str = "chroma"
    EMBEDDINGS_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    USE_OPENAI_EMBEDDINGS: bool = False
    OPENAI_API_KEY: str | None = None
    PINECONE_API_KEY: str | None = None
    PINECONE_INDEX: str = "ai-invest"

    class Config:
        env_file_encoding = "utf-8"
        case_sensitive = True

    def __init__(self, **values):
        super().__init__(**values)
        # Strip all string values to remove trailing spaces
        for k, v in values.items():
            if isinstance(v, str):
                setattr(self, k, v.strip())
        # Convert "true"/"false" strings to bool
        if isinstance(self.USE_OPENAI_EMBEDDINGS, str):
            self.USE_OPENAI_EMBEDDINGS = self.USE_OPENAI_EMBEDDINGS.lower() == "true"

settings = Settings()

print("DEBUG: OPENAI_API_KEY loaded =", settings.OPENAI_API_KEY[:8] + "..." if settings.OPENAI_API_KEY else "None")
print("DEBUG: USE_OPENAI_EMBEDDINGS =", settings.USE_OPENAI_EMBEDDINGS)
print("DEBUG: All env keys starting with OPENAI:", 
      {k: v for k, v in os.environ.items() if "OPENAI" in k})
