from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from app.services.llm_service import GeminiLLM
from app.models.schemas import Feedback

router = APIRouter(
    prefix="/llm",
    tags=["LLM"]
)

# --- Requête LLM ---
class LLMRequest(BaseModel):
    candidates: List[str]
    feedback_history: Optional[List[Dict]] = []
    word_length: int = 5
    language: str = "fr"

# --- Réponse LLM ---
class LLMResponse(BaseModel):
    suggested_word: str
    explanation: str

# --- Service LLM ---
llm_service = GeminiLLM()

@router.post("/suggest", response_model=LLMResponse)
async def suggest_word(req: LLMRequest):
    if not req.candidates:
        raise HTTPException(status_code=400, detail="Liste des candidats vide")

    try:
        word, explanation = llm_service.suggest_word(
            candidates=req.candidates,
            feedback_history=req.feedback_history,
            word_length=req.word_length,
            language=req.language
        )
        return LLMResponse(suggested_word=word, explanation=explanation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur LLM : {str(e)}")
