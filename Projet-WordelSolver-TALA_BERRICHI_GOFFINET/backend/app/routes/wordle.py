from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.data.load_fr_word import load_fr_words
from app.data.load_en_word import load_en_words
from app.services.wordle_solver import HybridWordleSolver
from app.models.schemas import Feedback
from app.services.llm_service import GeminiLLM

router = APIRouter()

# Charger dictionnaires
words_fr = load_fr_words()
words_en = load_en_words()

solver_fr = HybridWordleSolver(words_fr)
solver_en = HybridWordleSolver(words_en)
llm_service = GeminiLLM()

class WordleRequest(BaseModel):
    feedback: Feedback
    language: Optional[str] = "fr"
    use_llm: Optional[bool] = False

@router.post("/guess")
def make_guess(req: WordleRequest):
    lang = (req.language or "fr").lower()
    solver = solver_fr if lang == "fr" else solver_en if lang == "en" else None
    if solver is None:
        raise HTTPException(status_code=400, detail="Langue non supportée.")

    solver.update_constraints(req.feedback.dict())
    next_guess, explanation = solver.get_next_guess(language=lang)

    # Si LLM demandé
    if req.use_llm:
        try:
            llm_word, llm_explanation = llm_service.suggest_word(
                candidates=solver.csp.filter_candidates(solver.constraints),
                feedback_history=[solver.constraints_dict()],
                word_length=5,
                language=lang
            )
            return {"next_guess": llm_word, "explanation": llm_explanation}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur LLM Gemini : {str(e)}")

    return {"next_guess": next_guess, "explanation": explanation}
