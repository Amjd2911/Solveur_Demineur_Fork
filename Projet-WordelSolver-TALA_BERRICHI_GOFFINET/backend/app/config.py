# backend/app/config.py
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Wordle Solver API"

    # Clé API Gemini LLM
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
    if GEMINI_API_KEY is None:
        raise ValueError("La clé GEMINI_API_KEY n'est pas définie dans le fichier .env")

    # Origines autorisées pour CORS
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",  # frontend Vite
        "http://localhost:3000"   # frontend CRA
    ]

    # Paramètres généraux (à adapter si besoin)
    DEFAULT_WORD_LENGTH: int = 5
    MAX_CANDIDATES: int = 1000

# Instance globale de settings
settings = Settings()
if __name__ == "__main__":
    print("Project Name:", settings.PROJECT_NAME)
    print("Gemini API Key:", settings.GEMINI_API_KEY)
    print("Allowed Origins:", settings.ALLOWED_ORIGINS)