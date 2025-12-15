# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import wordle, llm
from app.config import settings

app = FastAPI(title="Wordle Solver API")

# --- Middleware CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # utilise la liste de config
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routes ---
app.include_router(wordle.router, prefix="/wordle", tags=["Wordle"])
app.include_router(llm.router, prefix="/llm", tags=["LLM"])
