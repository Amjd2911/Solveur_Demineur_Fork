# Projet : Recherche Symbolique — Stable Marriage et Wordle

Ce dépôt contient des travaux de groupe portant sur l'analyse du problème du mariage stable (Stable Marriage) et un solveur Wordle. Le fichier principal pour l'analyse du mariage stable est `stable_marriage_analysis.ipynb`.

## Arborescence principale

- `Groupe13/` : documents du groupe (plan, sujet, notes).
- `stable_marriage_analysis.ipynb` : notebook principal qui contient :
  - l'implémentation de l'algorithme de Gale–Shapley,
  - un modèle CSP (OR-Tools CP-SAT) pour trouver des mariages stables,
  - des fonctions de génération d'instances, validation de stabilité, benchmarks et visualisations.
- `wordle-solver/` : code du solveur Wordle (backend, frontend d'exemple, stratégies, utilitaires et dépendances). Contient aussi des scripts d'exécution et `requirements.txt` pour ce sous-projet.
- `wordle_solver/` : package Python pour le solveur Wordle (algorithmes, CSP, dictionnaires, stratégies).
- `tests/` : tests automatisés (par ex. `tests/test_stable_marriage.py`) pour vérifier la cohérence entre le modèle CSP et l'algorithme de référence.
- `LICENSE` : licence du dépôt.

## Fichier principal

Ouvrez et exécutez `stable_marriage_analysis.ipynb` pour :
- générer des préférences aléatoires,
- comparer la sortie du modèle CSP avec l'algorithme de Gale–Shapley,
- visualiser et benchmarker les performances.

Le notebook est autonome et contient des cellules d'explication et de visualisation. Si vous utilisez VS Code, ouvrez le notebook et exécutez les cellules dans l'ordre.

## Dépendances et exécution (Windows)

1. Créer et activer un environnement virtuel (PowerShell) :

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Installer les dépendances nécessaires (exemples) :

```powershell
pip install -r wordle-solver/requirements.txt
pip install ortools nbformat pytest matplotlib networkx seaborn
```

3. Lancer les tests unitaires (ex. test du mariage stable) :

```powershell
.venv\Scripts\python.exe -m pytest -q tests/test_stable_marriage.py
```

Remarque : certains sous-dossiers (comme `wordle-solver/backend`) ont leurs propres `requirements.txt` qui peuvent être utilisés pour installer des dépendances spécifiques.

## Tests et validation

Le test principal ajouté vérifie que le modèle CSP trouve une solution stable et la compare à l'algorithme de Gale–Shapley sur une instance réduite. Voir `tests/test_stable_marriage.py` pour les détails.
