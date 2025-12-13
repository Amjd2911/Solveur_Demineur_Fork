# backend/app/main.py
from fastapi import FastAPI
from app.routes import wordle, llm

app = FastAPI(title="Wordle Solver API")

# Route pour le solveur Wordle CSP + LLM
app.include_router(wordle.router, prefix="/wordle", tags=["Wordle"])

# Route spécifique pour LLM (suggestions de mots)
app.include_router(llm.router, prefix="/llm", tags=["LLM"])
