from typing import List, Dict, Tuple, Optional
from app.services.csp_solver import CSPSolver, WordleConstraints
from app.services.llm_service import GeminiLLM
from app.services.utils import generate_word_from_constraints

class HybridWordleSolver:
    """Solveur hybride Wordle : CSP + LLM"""
    def __init__(self, word_list: List[str], api_key: Optional[str] = None):
        self.word_list = word_list
        self.constraints = WordleConstraints()
        self.past_guesses: List[str] = []

        # Solveur CSP
        self.csp = CSPSolver(word_length=5)
        self.csp.set_valid_words(word_list)

        # LLM
        self.llm = GeminiLLM(api_key=api_key)

    def update_constraints(self, feedback: Dict):
        """Met à jour les contraintes avec le dernier feedback"""
        self.constraints.update(feedback)

    def constraints_dict(self) -> Dict:
        """Convertit les contraintes en dict pour le LLM"""
        return {
            "green": self.constraints.green,
            "yellow": {k: list(v) for k, v in self.constraints.yellow.items()},
            "grey": list(self.constraints.grey),
            "min_letter_counts": self.constraints.min_letter_counts
        }

    def get_next_guess(self, language: str = "fr") -> Tuple[str, str]:
        """Retourne le mot suivant et une explication"""
        candidates = self.csp.filter_candidates(self.constraints)
        if not candidates:
            fallback_word = generate_word_from_constraints(self.constraints_dict())
            return fallback_word, "Mot généré par fallback"

        word, explanation = self.llm.suggest_word(
            candidates=candidates,
            feedback_history=[self.constraints_dict()],
            word_length=5,
            language=language
        )
        self.past_guesses.append(word)
        return word, explanation

    def play_round(self, feedback: Dict, language: str = "fr") -> Tuple[str, str]:
        self.update_constraints(feedback)
        return self.get_next_guess(language=language)
