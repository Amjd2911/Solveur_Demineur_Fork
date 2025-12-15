# backend/app/data/word_generator.py
import random
from typing import List

def choose_secret_candidate(candidates: List[str]) -> str:
    """
    Sélectionne un mot aléatoire (chaîne de 5 lettres) depuis le dictionnaire fourni.

    :param candidates: Liste de mots valides.
    :return: Mot choisi aléatoirement en majuscules.
    """
    if not candidates:
        raise ValueError("Le dictionnaire de candidats est vide.")
    return random.choice(candidates).upper()


def choose_secret_word(
    language: str,
    fr_candidates: List[str],
    en_candidates: List[str]
) -> str:
    """
    Sélectionne le mot secret Wordle depuis le dictionnaire
    correspondant à la langue choisie.

    :param language: "fr" ou "en"
    :param fr_candidates: Liste de mots français
    :param en_candidates: Liste de mots anglais
    :return: Mot secret choisi aléatoirement
    """
    language = language.lower()

    if language == "fr":
        return choose_secret_candidate(fr_candidates)

    elif language == "en":
        return choose_secret_candidate(en_candidates)

    else:
        raise ValueError("Langue invalide : choisir 'fr' ou 'en'.")


# Test rapide si on exécute ce fichier directement
if __name__ == "__main__":
    from load_fr_word import load_fr_words
    from load_en_word import load_en_words

    fr_words = load_fr_words()
    en_words = load_en_words()

    print("Mot secret FR :", choose_secret_word("fr", fr_words, en_words))
    print("Mot secret EN :", choose_secret_word("en", fr_words, en_words))
