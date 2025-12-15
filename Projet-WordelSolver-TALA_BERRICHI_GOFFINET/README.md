# 🧩 Wordle Solver

## Description

**Wordle Solver** est une application web interactive qui aide les utilisateurs à résoudre le célèbre jeu **Wordle** grâce à plusieurs stratégies complémentaires :

* **CSP Solver** : résolution par programmation par contraintes (*Constraint Satisfaction Problem*).
* **LLM Solver** : suggestions générées par un modèle de langage (LLM).
* **CSP + LLM** : approche hybride combinant rigueur algorithmique et raisonnement linguistique.

L’application permet de jouer à Wordle directement dans le navigateur, de comparer les solveurs et de suivre ses performances dans une interface moderne et responsive.

---

## ✨ Fonctionnalités

* 🎮 Jouer à Wordle directement depuis le navigateur.
* 🤖 Suggestions automatiques de mots via :

  * CSP Solver
  * LLM Solver
  * CSP + LLM Solver
  
* 🧠 Évaluation automatique des propositions (vert / jaune / gris).
* 🕒 Historique des mots joués et de leurs résultats.
* 🌙 Thème clair / sombre.
* 📱 Interface moderne, responsive et accessible.

---

## 🛠️ Tech Stack

### Frontend

* **React 19**
* **Tailwind CSS**
* **Sonner** (notifications)

### Backend

* **Python – FastAPI** *(ou Node.js + Express selon la version)*
* API pour :

  * Évaluation des mots
  * Suggestions CSP / LLM / CSP+LLM

### Autres

* **LLM** (ex. Gemini ou GPT) pour la génération de suggestions intelligentes
* **CSP Solver** pour Wordle (contraintes sur lettres, positions et occurrences)
* **MongoDB** *(optionnel)* pour le stockage des statistiques

---

## 🚀 Installation

### 1️⃣ Cloner le dépôt

```bash
git clone https://github.com/Safae-Berr/2025-MSMIN5IN52-Search-Symbolic-Min1.git
cd Projet-WordelSolver-TALA_BERRICHI_GOFFINET
```

---

### 2️⃣ Backend

```bash
# Naviguer vers le dossier backend
cd backend

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Sur Windows:
venv\Scripts\activate
# Sur Mac/Linux:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement 
copy .env.exemple .env

# Le backend sera disponible sur :
http://localhost:8000
```

---

### 3️⃣ Frontend

```bash
cd frontend
# Installer les dépendances
npm install

# Lancer le serveur
npm run dev
```

# Ouvrez ensuite votre navigateur sur :
http://localhost:5173

---

## 🎯 Utilisation

1. Cliquez sur les lettres du clavier virtuel (ou utilisez le clavier physique).
2. Appuyez sur **Entrée** pour soumettre un mot.
3. Choisissez un solver :

   * **CSP** : calcule la meilleure suggestion basée sur des contraintes.
   * **LLM** : génère une suggestion via un modèle de langage.
   * **CSP + LLM** : combine les deux approches pour un choix optimal.
4. Analysez le feedback sur le plateau :

   * 🟩 **Vert** : lettre correcte et bien placée.
   * 🟨 **Jaune** : lettre correcte mais mal placée.
   * ⬜ **Gris** : lettre absente du mot.

---

## 📁 Structure du projet

```text
Projet-WordelSolver-TALA_BERRICHI_GOFFINET/
│
├─ backend/                 # API FastAPI ou Express
│  ├─ app/
│  │  ├─ main.py            # Point d'entrée du serveur
│  │  ├─ services/
│  │  │  ├─ csp_solver.py
│  │  │  ├─ csp_llm_solver.py
│  │  │  ├─ llm_service.py
│  │  │  └─ utils.py
│  │  └─ data/
│  └─ requirements.txt
│
├─ frontend/                # Application React
│  ├─ src/
│  │  ├─ components/
│  │  │  ├─ GameBoard.jsx
│  │  │  ├─ GameTile.jsx
│  │  │  ├─ Keyboard.jsx
│  │  │  ├─ SolverPanel.jsx
│  │  │  └─ GameStats.jsx
│  │  ├─ utils/
│  │  ├─ App.jsx
│  │  └─ main.jsx
│  ├─ package.json
│  └─ tailwind.config.js
│
└─ README.md
```

---

## Collaborateurs : 
Safae BERRICHI
Lamyae TALA 
Pauline GOFFINET

## 📜 Licence

Ce projet est open-source. Vous pouvez l’utiliser, le modifier et le distribuer librement.
👨‍💻 Projet académique / expérimental autour de l’IA, des CSP et du développement web moderne.