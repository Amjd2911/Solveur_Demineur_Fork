from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import random

from app.data.load_fr_word import load_fr_words
from app.data.load_en_word import load_en_words
from app.services.csp_solver import CSPSolver, WordleConstraints
from app.services.csp_llm_solver import HybridWordleSolver
from app.services.llm_service import GeminiLLM
from app.models.schemas import Feedback, WordSuggestionsRequest

router = APIRouter()

# ------------------------
# Chargement des dictionnaires
# ------------------------
words_fr = load_fr_words()
words_en = load_en_words()

# ------------------------
# Solveurs CSP seuls
# ------------------------
csp_solver_fr = CSPSolver(word_length=5)
csp_solver_fr.set_valid_words(words_fr)

csp_solver_en = CSPSolver(word_length=5)
csp_solver_en.set_valid_words(words_en)

# ------------------------
# Solveurs hybrides CSP + LLM
# ------------------------
hybrid_solver_fr = HybridWordleSolver(words_fr)
hybrid_solver_en = HybridWordleSolver(words_en)

# Service LLM
llm_service = GeminiLLM()


class WordleRequest(BaseModel):
    feedback: Feedback
    language: Optional[str] = "fr"


# ------------------------
# Fonction utilitaire pour initialiser une partie
# ------------------------
def start_new_game(solver, word_list):
    """Réinitialise les contraintes et choisit un mot secret aléatoire"""
    solver.reset()  # pour HybridWordleSolver
    if isinstance(solver, CSPSolver):
        solver.secret_word = random.choice(word_list)
    else:
        solver.secret_word = random.choice(word_list)


# ============================================================
# ROUTE 1 — CSP SEUL
# ============================================================
@router.post("/guess/csp")
def guess_csp(req: WordleRequest):
    lang = (req.language or "fr").lower()
    solver = csp_solver_fr if lang == "fr" else csp_solver_en if lang == "en" else None
    word_list = words_fr if lang == "fr" else words_en

    if solver is None:
        raise HTTPException(status_code=400, detail="Langue non supportée.")

    # ⚡ Nouvelle partie si pas de mot secret
    if not hasattr(solver, "secret_word"):
        start_new_game(solver, word_list)

    # ⚡ Générer les contraintes locales à partir du feedback
    constraints = WordleConstraints()
    constraints.update(req.feedback.dict())

    candidates = solver.filter_candidates(constraints)

    if not candidates:
        return {
            "next_guess": "aaaaa",
            "explanation": "Fallback : aucun mot valide CSP"
        }

    # ⚡ Choisir un mot aléatoire parmi les candidats
    next_guess = random.choice(candidates)
    return {
        "next_guess": next_guess,
        "explanation": f"Mot proposé par CSP seul (mot secret : {solver.secret_word})"
    }


# ============================================================
# ROUTE 2 — CSP + LLM (HYBRIDE)
# ============================================================
@router.post("/guess/hybrid")
def guess_hybrid(req: WordleRequest):
    lang = (req.language or "fr").lower()
    solver = hybrid_solver_fr if lang == "fr" else hybrid_solver_en if lang == "en" else None
    word_list = words_fr if lang == "fr" else words_en

    if solver is None:
        raise HTTPException(status_code=400, detail="Langue non supportée.")

    # ⚡ Nouvelle partie si pas de mot secret
    if not hasattr(solver, "secret_word"):
        start_new_game(solver, word_list)

    # ⚡ Mettre à jour les contraintes du solveur hybride
    solver.update_constraints(req.feedback.dict())

    try:
        candidates = solver.csp.filter_candidates(solver.constraints)

        if not candidates:
            return {
                "next_guess": "aaaaa",
                "explanation": "Fallback : aucun candidat CSP"
            }

        # ⚡ LLM propose un mot parmi les candidats
        llm_word, llm_explanation = llm_service.suggest_word(
            candidates=list(candidates)[:50],
            feedback_history=[solver.constraints_dict()],
            word_length=5,
            language=lang
        )

        return {
            "next_guess": llm_word,
            "explanation": f"{llm_explanation} (mot secret : {solver.secret_word})"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# ROUTE 3 — SUGGESTION IA (OPTIONNELLE)
# ============================================================
@router.post("/suggest-ai")
def suggest_with_ai(req: WordSuggestionsRequest):
    lang = req.language.lower()
    solver = hybrid_solver_fr if lang == "fr" else hybrid_solver_en if lang == "en" else None

    if solver is None:
        raise HTTPException(status_code=400, detail="Langue non supportée.")

    solver.update_constraints(req.feedback.dict())
    candidates = solver.csp.filter_candidates(solver.constraints)

    if not candidates:
        raise HTTPException(
            status_code=400,
            detail="Aucun candidat trouvé avec ces contraintes"
        )

    llm_word, llm_explanation = llm_service.suggest_word(
        candidates=list(candidates)[:50],
        feedback_history=[],
        word_length=5,
        language=lang
    )

    return {
        "suggested_word": llm_word.upper(),
        "explanation": llm_explanation,
        "candidates_count": len(candidates)
    }
