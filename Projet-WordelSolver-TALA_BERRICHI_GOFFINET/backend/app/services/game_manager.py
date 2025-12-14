# backend/app/services/game_manager.py
from typing import List, Dict, Tuple, Optional, Set, Union
from app.services.csp_solver import CSPSolver, WordleConstraints
from app.services.csp_llm_solver import HybridWordleSolver
from app.services.utils import generate_word_from_constraints
from app.data.load_en_word import load_en_words
from app.data.load_fr_word import load_fr_words
from app.data.word_generator import choose_secret_word
from typing import cast

# Type pour le feedback Wordle
FeedbackType = Dict[str, Union[Dict[int, str], Dict[int, Set[str]], List[str]]]

MAX_ATTEMPTS = 6  # Limite de tentatives

class GameManager:
    """Gestion des parties Wordle avec choix du solveur (CSP seul ou CSP+LLM)"""

    def __init__(self, language: str = "fr", use_llm: bool = False, api_key: Optional[str] = None):
        self.language = language.lower()
        self.use_llm = use_llm
        self.api_key = api_key

        # Charger les mots selon la langue
        if self.language == "fr":
            self.word_list = load_fr_words()
        elif self.language == "en":
            self.word_list = load_en_words()
        else:
            raise ValueError("Langue invalide : choisir 'fr' ou 'en'")

        self.word_length = 5
        self.secret_word: str = ""
        self.attempts: int = 0
        self.solver: Optional[Union[CSPSolver, HybridWordleSolver]] = None

    def start_new_game(self):
        """Initialise une nouvelle partie avec un mot aléatoire et reset du solveur"""
        self.secret_word = choose_secret_word(
            language=self.language,
            fr_candidates=self.word_list if self.language == "fr" else [],
            en_candidates=self.word_list if self.language == "en" else []
        ).lower()

        self.attempts = 0

        if self.use_llm:
            self.solver = HybridWordleSolver(self.word_list, api_key=self.api_key)
        else:
            self.solver = CSPSolver(word_length=self.word_length)
            self.solver.set_valid_words(self.word_list)

        print(f"[DEBUG] Mot secret ({self.language}): {self.secret_word}")  # Pour debug

    def make_guess(self, guess: str) -> FeedbackType:
        """Fait une tentative et renvoie le feedback"""
        guess = guess.lower()

        # Vérifie si la limite de tentatives est atteinte
        if self.attempts >= MAX_ATTEMPTS:
            raise Exception(f"Nombre maximum de tentatives ({MAX_ATTEMPTS}) atteint")

        # Vérifie que le mot est valide
        if guess not in self.word_list:
            raise ValueError(f"Mot invalide : {guess}")

        self.attempts += 1
        feedback = self.compute_feedback(guess)

        # Met à jour les contraintes si solveur hybride
        if isinstance(self.solver, HybridWordleSolver):
            self.solver.update_constraints(feedback)

        return feedback

    def compute_feedback(self, guess: str) -> FeedbackType:
        """Calcule le feedback Wordle (green, yellow, grey) de manière robuste"""
        feedback: FeedbackType = {
            "green": {},    # Dict[int, str]
            "yellow": {},   # Dict[int, Set[str]]
            "grey": []      # List[str]
        }

        secret_counts: Dict[str, int] = {}
        for letter in self.secret_word:
            secret_counts[letter] = secret_counts.get(letter, 0) + 1

        # Lettres vertes
        green = cast(Dict[int, str], feedback["green"])
        for i, (g, t) in enumerate(zip(guess, self.secret_word)):
            if g == t:
                green[i] = g
                secret_counts[g] -= 1

        # Lettres jaunes et grises
        yellow = cast(Dict[int, Set[str]], feedback["yellow"])
        grey = cast(List[str], feedback["grey"])
        for i, g in enumerate(guess):
            if i in green:
                continue
            if g in secret_counts and secret_counts[g] > 0:
                if i not in yellow:
                    yellow[i] = set()
                yellow[i].add(g)
                secret_counts[g] -= 1
            else:
                grey.append(g)

        return feedback

    def is_correct_guess(self, guess: str) -> bool:
        """Vérifie si le mot proposé est correct"""
        return guess.lower() == self.secret_word.lower()

    def get_solver_guess(self) -> Tuple[str, str]:
        """Demande au solveur de proposer un mot"""
        if isinstance(self.solver, HybridWordleSolver):
            return self.solver.get_next_guess(language=self.language)
        elif isinstance(self.solver, CSPSolver):
            candidates = self.solver.filter_candidates()
            if not candidates:
                fallback_word = generate_word_from_constraints({})
                return fallback_word, "Mot généré fallback"
            return candidates[0], "Mot proposé par CSP"
        else:
            raise ValueError("Solveur inconnu")

    def get_attempts(self) -> int:
        """Retourne le nombre de tentatives effectuées"""
        return self.attempts
