# backend/app/services/llm_service.py
from typing import List, Dict, Optional, Tuple
import os
import requests

class GeminiLLM:
    """
    Service d'intégration d'un LLM (Google Gemini / AI Studio) pour suggérer des mots Wordle
    """
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-1.5-mini"):
        # Clé API
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("La clé API Gemini n'est pas définie (GEMINI_API_KEY)")
        self.model = model
        # Endpoint pour Gemini / PaLM API
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta2/models/{self.model}:generateMessage"

    def suggest_word(
        self,
        candidates: List[str],
        feedback_history: Optional[List[Dict]] = None,
        word_length: int = 5,
        language: str = "fr"
    ) -> Tuple[str, str]:
        """
        Retourne le mot suggéré par le LLM selon les candidats filtrés et les feedbacks précédents.

        Args:
            candidates: liste des mots valides filtrés par CSP
            feedback_history: liste de feedbacks précédents au format {green, yellow, grey}
            word_length: longueur du mot
            language: "fr" ou "en"

        Returns:
            (mot_suggere, explication)
        """
        feedback_history = feedback_history or []

        # Construire le prompt pour le LLM
        prompt = f"""
Tu es un expert Wordle {language.upper()}.
Tu dois proposer le mot suivant à deviner parmi une liste de candidats.
Liste des candidats possibles (max 50 affichés): {', '.join(candidates[:50])}...
Feedbacks précédents: {feedback_history}

Répond uniquement par le mot suivant à deviner et donne une courte explication de ton choix.
"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "prompt": {
                "messages": [
                    {"author": "user", "content": prompt}
                ]
            },
            "temperature": 0.2,
            "max_output_tokens": 20
        }

        # Appel HTTP vers Gemini
        try:
            response = requests.post(self.endpoint, json=payload, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            raise ConnectionError(f"Erreur de connexion au LLM Gemini: {e}")

        try:
            data = response.json()
            # Extraction du mot et de l'explication depuis la réponse
            content = data['candidates'][0]['content'][0]['text'].strip()
            parts = content.split(None, 1)  # Séparer le mot et l'explication
            word = parts[0].lower()
            explanation = parts[1].strip() if len(parts) > 1 else "Aucune explication fournie"
            return word, explanation
        except (KeyError, IndexError, Exception) as e:
            raise ValueError(f"Impossible d'extraire le mot du LLM Gemini: {e}")
