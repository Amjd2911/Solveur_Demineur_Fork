from ortools.sat.python import cp_model
from typing import List, Dict, Set, Optional
from collections import defaultdict, Counter

class WordleConstraints:
    """Stocke les contraintes du jeu Wordle"""
    def __init__(self):
        self.green: Dict[int, str] = {}
        self.yellow: Dict[int, Set[str]] = defaultdict(set)
        self.grey: Set[str] = set()
        self.min_letter_counts: Dict[str, int] = {}

    def update(self, feedback: Dict):
        green = feedback.get("green", {})
        yellow = feedback.get("yellow", {})
        grey = feedback.get("grey", [])

        for pos, letter in green.items():
            self.green[pos] = letter

        for pos, letters in yellow.items():
            self.yellow[pos].update(letters)

        for letter in grey:
            self.grey.add(letter)

        counts = Counter(list(green.values()) + [l for letters in yellow.values() for l in letters])
        for letter, count in counts.items():
            self.min_letter_counts[letter] = max(self.min_letter_counts.get(letter, 0), count)


class CSPSolver:
    """Solveur CSP Wordle"""
    def __init__(self, word_length: int = 5):
        self.word_length = word_length
        self.word_list: List[str] = []
        self.letter_set: Set[str] = set()

    def set_valid_words(self, words: List[str]):
        self.word_list = [w.lower() for w in words if len(w) == self.word_length]
        self.letter_set = set("".join(self.word_list))

    def filter_candidates(self, constraints: Optional[WordleConstraints] = None, max_solutions: int = 1000) -> List[str]:
        """Retourne la liste de mots qui respectent les contraintes"""
        candidates = []
        for word in self.word_list:
            if constraints is None or self._check_word(word, constraints):
                candidates.append(word)
                if len(candidates) >= max_solutions:
                    break
        return candidates

    def _check_word(self, word: str, constraints: WordleConstraints) -> bool:
        for pos, letter in constraints.green.items():
            if word[pos] != letter:
                return False

        for pos, letters in constraints.yellow.items():
            for letter in letters:
                if word[pos] == letter or letter not in word:
                    return False

        for letter in constraints.grey:
            if letter in word and letter not in constraints.green.values() and all(letter not in lset for lset in constraints.yellow.values()):
                return False

        for letter, min_count in constraints.min_letter_counts.items():
            if word.count(letter) < min_count:
                return False

        return True
