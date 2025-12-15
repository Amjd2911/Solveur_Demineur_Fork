import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("La clé API Gemini n'est pas définie.")

# Endpoint pour vérifier l'usage
endpoint = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

try:
    response = requests.get(endpoint, timeout=10)
    response.raise_for_status()
    data = response.json()
    print("✅ Clé API valide !")
    
    # Afficher les modèles et éventuellement les quotas si disponibles
    if "models" in data:
        for model in data["models"]:
            print(model)
    else:
        print("Aucune info de modèle disponible.")
        
except requests.RequestException as e:
    print(f"❌ Erreur API ou quota atteint : {e}")
