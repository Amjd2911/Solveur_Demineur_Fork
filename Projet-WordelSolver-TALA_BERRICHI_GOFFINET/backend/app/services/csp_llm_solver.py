# backend/app/services/csp_llm_solver.py
from typing import List, Dict, Tuple, Optional
from app.services.csp_solver import CSPSolver, WordleConstraints
from app.services.llm_service import GeminiLLM
from app.services.utils import generate_word_from_constraints


class HybridWordleSolver:
    """Solveur hybride Wordle : CSP + LLM"""

    def __init__(self, word_list: List[str], api_key: Optional[str] = None, word_length: int = 5):
        self.word_length = word_length
        self.word_list = [w.lower() for w in word_list if len(w) == self.word_length]
        self.constraints = WordleConstraints()
        self.past_guesses: List[str] = []
        self.secret_word: Optional[str] = None 

        # Solveur CSP
        self.csp = CSPSolver(word_length=self.word_length)
        self.csp.set_valid_words(self.word_list)

        # LLM
        self.llm = GeminiLLM(api_key=api_key)

    def update_constraints(self, feedback: Dict):
        """Met à jour les contraintes avec le dernier feedback"""
        self.constraints.update(feedback)

    def constraints_dict(self) -> Dict:
        """Convertit les contraintes en dictionnaire pour le LLM"""
        return {
            "green": self.constraints.green,
            "yellow": {k: list(v) for k, v in self.constraints.yellow.items()},
            "grey": list(self.constraints.grey),
            "min_letter_counts": self.constraints.min_letter_counts
        }

    def get_next_guess(self, language: str = "fr") -> Tuple[str, str]:
        """
        Retourne le mot suivant et une explication.
        Combine CSP + LLM pour sélectionner le mot optimal.
        """
        # Étape 1 : Filtrage CSP
        candidates = self.csp.filter_candidates(self.constraints)
        
        # Étape 2 : Fallback si aucun mot n’est valide
        if not candidates:
            fallback_word = generate_word_from_constraints(self.constraints_dict())
            return fallback_word, "Mot généré par fallback (aucun candidat CSP valide)"

        # Étape 3 : Suggestion LLM parmi les candidats filtrés
        try:
            word, explanation = self.llm.suggest_word(
                candidates=candidates,
                feedback_history=[self.constraints_dict()],
                word_length=self.word_length,
                language=language
            )
        except Exception as e:
            # En cas d’erreur LLM, prendre le premier candidat CSP
            word, explanation = candidates[0], f"Mot par défaut (erreur LLM : {e})"

        self.past_guesses.append(word.lower())
        return word.lower(), explanation

    def play_round(self, feedback: Dict, language: str = "fr") -> Tuple[str, str]:
        """
        Joue un tour : met à jour les contraintes et retourne le prochain mot.
        """
        self.update_constraints(feedback)
        return self.get_next_guess(language=language)

    def reset(self):
        """
        Réinitialise le solveur pour une nouvelle partie.
        """
        self.constraints = WordleConstraints()
        self.past_guesses.clear()
