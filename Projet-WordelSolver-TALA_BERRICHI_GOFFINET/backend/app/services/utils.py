# backend/app/services/utils.py
from typing import List, Dict

def filter_candidates(word_list: List[str], constraints: Dict) -> List[str]:
    """
    Filtre la liste des candidats selon les contraintes imposées par Wordle (vert, jaune, gris, etc.).

    :param word_list: Liste de mots candidats.
    :param constraints: Dictionnaire de contraintes (vert, jaune, gris, min_letter_counts).
    :return: Liste des mots valides après application des contraintes.
    """
    candidates = []

    for word in word_list:
        word_lower = word.lower()
        valid = True

        # Vertes : Lettres à la bonne position
        for pos, letter in constraints.get("green", {}).items():
            if pos >= len(word_lower) or word_lower[pos] != letter:
                valid = False
                break

        # Jaunes : Lettres présentes mais pas à cette position
        for pos, letters in constraints.get("yellow", {}).items():
            if pos < len(word_lower) and word_lower[pos] in letters:
                valid = False
                break
            for letter in letters:
                if letter not in word_lower:
                    valid = False
                    break

        # Grises : Lettres absentes
        for letter in constraints.get("grey", []):
            if letter in word_lower:
                valid = False
                break

        # Occurrences minimales : Lettres devant apparaître un nombre minimum de fois
        for letter, count in constraints.get("min_letter_counts", {}).items():
            if word_lower.count(letter) < count:
                valid = False
                break

        if valid:
            candidates.append(word)

    return candidates


def score_word(word: str, letter_frequencies: Dict[str, int]) -> int:
    """
    Calcule un score pour un mot donné en fonction de la fréquence de ses lettres.
    Cette fonction est utile pour choisir le mot qui couvre le mieux les lettres les plus fréquentes.

    :param word: Le mot à évaluer.
    :param letter_frequencies: Fréquence des lettres dans les candidats restants.
    :return: Un score basé sur les fréquences des lettres du mot.
    """
    score = 0
    seen = set()

    for letter in word.lower():
        if letter not in seen:
            score += letter_frequencies.get(letter, 0)
            seen.add(letter)

    return score


def compute_letter_frequencies(word_list: List[str]) -> Dict[str, int]:
    """
    Calcule la fréquence de chaque lettre dans la liste des mots candidats.

    :param word_list: Liste de mots candidats.
    :return: Dictionnaire avec les lettres comme clés et leurs fréquences comme valeurs.
    """
    letter_frequencies = {}

    for word in word_list:
        for letter in set(word.lower()):  # Utiliser set pour éviter les doublons dans un mot
            letter_frequencies[letter] = letter_frequencies.get(letter, 0) + 1

    return letter_frequencies


def generate_feedback(guess: str, target_word: str) -> List[str]:
    """
    Génère le feedback Wordle (vert, jaune, gris) en comparant un mot proposé avec le mot cible.

    :param guess: Le mot proposé.
    :param target_word: Le mot cible.
    :return: Liste de feedback ('green', 'yellow', 'grey') pour chaque lettre du mot proposé.
    """
    feedback = [''] * len(guess)
    counts = {}

    # Pass 1: Vérification des lettres vertes
    for i, (g, t) in enumerate(zip(guess, target_word)):
        if g == t:
            feedback[i] = 'green'
            counts[g] = counts.get(g, 0) + 1

    # Pass 2: Vérification des lettres jaunes et grises
    for i, g in enumerate(guess):
        if feedback[i] == '':
            if g in target_word and target_word.count(g) > counts.get(g, 0):
                feedback[i] = 'yellow'
                counts[g] = counts.get(g, 0) + 1
            else:
                feedback[i] = 'grey'

    return feedback


def generate_word_from_constraints(constraints: Dict) -> str:
    """
    Génère un mot de substitution en respectant les contraintes (vert, jaune, gris).
    Utilisé pour créer un mot de secours si les candidats valides sont trop réduits.

    :param constraints: Dictionnaire contenant les contraintes de position (vert, jaune, gris).
    :return: Un mot respectant les contraintes, ou un mot par défaut.
    """
    word = ['_'] * 5  # Le mot est supposé avoir 5 lettres (modifiez en fonction de la taille de mot)
    for pos, letter in constraints.get("green", {}).items():
        word[pos] = letter

    # Remplir les cases restantes avec des lettres non grisées
    for i in range(len(word)):
        if word[i] == '_':
            for letter in "etaoinshrdlcumfwypvbgkjqxz":  # Utiliser les lettres les plus courantes
                if letter not in constraints.get("grey", []):
                    word[i] = letter
                    break

    return ''.join(word)

