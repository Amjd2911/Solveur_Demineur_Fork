# Optimisation de Tournées de Livraison (VRP)

## 📋 Présentation du projet

Ce projet propose une solution complète pour l'optimisation de tournées de véhicules (Vehicle Routing Problem, VRP) avec une interface web interactive. Le système supporte deux variantes principales :

- **VRP Classique** : optimisation avec contraintes de capacité et fenêtres temporelles
- **VRP Vert (E-VRP)** : optimisation pour véhicules électriques avec contraintes d'autonomie et stations de recharge

### Fonctionnalités principales

- ✅ Interface web interactive avec visualisation cartographique
- ✅ Résolution en temps réel avec suivi de progression
- ✅ Support de multiples véhicules avec capacités individuelles
- ✅ Contraintes de capacité et fenêtres temporelles
- ✅ Gestion de l'autonomie pour véhicules électriques
- ✅ Visualisation des tournées sur carte interactive (Leaflet)
- ✅ Calcul de distances réelles avec formule de Haversine (GPS)

### Technologies utilisées

- **Backend** : Python 3.12+, Flask, OR-Tools CP-SAT
- **Frontend** : HTML5, JavaScript, Leaflet.js
- **Optimisation** : Google OR-Tools (Constraint Programming - Satisfiability)
- **Visualisation** : Leaflet

---

## 👥 Présentation du groupe

**Membres du projet :**
- Alexis DHERMY
- Clément CARON
- Grégoire BRUN

**Contexte :**
Projet développé dans le cadre du cours d'Intelligence Artificielle II à l'EPF.

---

## 🚀 Installation et lancement du code

### Prérequis

- Python 3.12 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Naviguer vers le répertoire du projet**
   ```bash
   cd VRP-Alexis-Clement-Gregoire
   ```

2. **Créer un environnement virtuel** (recommandé)
   ```bash
   python -m venv venv
   ```

3. **Activer l'environnement virtuel**
   
   Sur Windows (PowerShell) :
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   Sur Linux/Mac :
   ```bash
   source venv/bin/activate
   ```

4. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

### Lancement de l'application

```bash
python main.py
```

L'application démarre sur `http://localhost:5000`

### Utilisation de l'interface web

1. **Ouvrir le navigateur** à l'adresse `http://localhost:5000`
2. **Configurer le problème** :
   - Cliquer sur la carte pour définir le dépôt (point de départ)
   - Ajouter des clients en cliquant sur la carte
   - Pour le VRP vert, ajouter des stations de recharge
   - Configurer les paramètres (nombre de véhicules, capacité, etc.)
3. **Lancer l'optimisation** : cliquer sur "Résoudre"
4. **Visualiser les résultats** : les tournées s'affichent automatiquement sur la carte

### Paramètres configurables

- **Nombre de véhicules** : nombre de véhicules disponibles
- **Type VRP** : classique ou vert (électrique)
- **Capacité** : capacité maximale de chaque véhicule (1 client = 10 unités de capacité par défaut)
- **Autonomie** : autonomie maximale de la batterie des véhicules électriques (10 km par défaut)
- **Taille des colis** : taille de chaque colis pour chaque client
- **Fenêtres temporelles** : heure de début et fin de disponibilité pour chaque client (par défaut 8h00-20h00, par tranches de 10 minutes)
- **Mode de raisonnement** : mode de raisonnement qui gère le temps de résolution (rapide, normal, exploratoire)

---

## 📚 Contexte, contenu théorique et technique

### Le problème VRP

Le **Vehicle Routing Problem (VRP)** est un problème d'optimisation combinatoire classique qui consiste à déterminer un ensemble de tournées optimales pour une flotte de véhicules devant servir un ensemble de clients à partir d'un dépôt central.

#### Formulation mathématique

Soit :
- $G = (V, E)$ un graphe avec $V = \{0, 1, ..., n\}$ (0 = dépôt, 1..n = clients)
- $d_{ij}$ : distance entre les nœuds $i$ et $j$
- $q_i$ : demande du client $i$
- $Q$ : capacité d'un véhicule
- $K$ : nombre de véhicules disponibles

**Objectif** : Minimiser la distance totale parcourue

**Contraintes** :
- Chaque client est visité exactement une fois
- Chaque véhicule part et revient au dépôt
- La somme des demandes sur une tournée ne dépasse pas $Q$
- Pas de sous-tours (connectivité)

### Variantes implémentées

#### VRP Classique (CVRP)

Extension du VRP avec :
- **Contraintes de capacité** : $\sum_{i \in T_k} q_i \leq Q$ pour chaque tournée $T_k$
- **Fenêtres temporelles** : chaque client $i$ doit être visité dans $[a_i, b_i]$ (configurable dans l'interface)
- **Temps de service** : temps constant de 10 minutes par client (10 unités de temps)
- **Conversion distance-temps** : 1 km parcouru = 5 minutes de trajet (5 unités de temps)

#### VRP Vert (E-VRP)

Extension pour véhicules électriques avec :
- **Contraintes d'autonomie** : niveau de batterie $B_i \geq 0$ à chaque nœud
- **Consommation** : $B_j = B_i - c \cdot d_{ij}$ où $c$ est la consommation
- **Stations de recharge** : possibilité de recharger à $B_{max}$ dans les stations
- **Temps de recharge** : temps nécessaire pour recharger complètement

### Méthode de résolution : OR-Tools CP-SAT

Le projet utilise **OR-Tools CP-SAT** (Constraint Programming - Satisfiability), une approche de programmation par contraintes qui :

1. Modélise le problème avec des variables de décision booléennes et entières
2. Définit les contraintes du problème
3. Utilise un solveur SAT pour trouver des solutions optimales ou réalisables

**Avantages** :
- Résolution exacte pour des problèmes de taille moyenne
- Gestion efficace des contraintes complexes
- Flexibilité pour ajouter de nouvelles contraintes

**Limitations** :
- Temps de résolution exponentiel dans le pire cas
- Nécessite des limites de temps pour les grands problèmes

### Ce qui a été mis en place dans le code

#### 1. Calcul des distances

Le système calcule les distances réelles entre les points GPS en utilisant la **formule de Haversine** :

```python
def _haversine_distance(self, lat1, lon1, lat2, lon2):
    """calcule la distance en kilomètres entre deux points GPS"""
    R = 6371.0  # rayon de la terre en kilomètres
    # conversion en radians et calcul de la distance
    ...
```

Cette méthode permet de calculer des distances précises sur la surface de la Terre plutôt que des distances euclidiennes planes.

#### 2. Modélisation CP-SAT

**Variables de décision** :

- **Variables booléennes `x[i, j, k]`** : indique si le véhicule `k` emprunte l'arc de `i` à `j`
  ```python
  x[i, j, k] = model.NewBoolVar(f'x_{i}_{j}_{k}')
  ```

- **Variables de position `position[i, k]`** : position du nœud `i` dans la tournée du véhicule `k` (évite les sous-tours)
  ```python
  position[i, k] = model.NewIntVar(0, self.n, f'pos_{i}_{k}')
  ```

- **Variables de temps `temps_arrivee[i, k]`** : temps d'arrivée du véhicule `k` au nœud `i`
  ```python
  temps_arrivee[i, k] = model.NewIntVar(0, 10000, f'time_{i}_{k}')
  ```

- **Variables de charge `charge[i, k]`** : charge du véhicule `k` au nœud `i`
  ```python
  charge[i, k] = model.NewIntVar(0, capacite_k, f'load_{i}_{k}')
  ```

- **Variables de batterie `batterie[i, k]`** (VRP vert uniquement) : niveau de batterie du véhicule `k` au nœud `i`
  ```python
  batterie[i, k] = model.NewIntVar(0, batterie_max_k, f'battery_{i}_{k}')
  ```

**Contraintes principales** :

1. **Contraintes de visite** : chaque client visité exactement une fois
   ```python
   for j in range(1, self.n):
       model.Add(sum(x[i, j, k] for i, k) == 1)
   ```

2. **Conservation de flux** : entrées = sorties pour chaque nœud
   ```python
   model.Add(
       sum(x[i, j, k] for i) == sum(x[j, i, k] for i)
   )
   ```

3. **Contraintes de capacité** : la charge augmente de la demande du client
   ```python
   model.Add(
       charge[j, k] >= charge[i, k] + demande_j - capacite_k * (1 - x[i, j, k])
   )
   ```

4. **Fenêtres temporelles** : temps d'arrivée dans la fenêtre autorisée
   ```python
   model.Add(temps_arrivee[j, k] >= debut)
   model.Add(temps_arrivee[j, k] <= fin)
   ```
   - Les fenêtres temporelles sont configurables dans l'interface (8h00-20h00 par défaut, par tranches de 10 minutes)
   - Le temps de référence 0 correspond à 8h00 du matin
   - Si un véhicule arrive avant le début de la fenêtre, il attend jusqu'à l'ouverture

5. **Contraintes temporelles de trajet** : temps d'arrivée = temps départ + temps trajet + temps service
   ```python
   # 1 km = 5 minutes (5 unités de temps)
   dist = int(self.distances[i][j] * 5)
   temps_serv = 10  # 10 minutes par défaut
   model.Add(temps_arrivee[j, k] >= temps_arrivee[i, k] + temps_serv + dist - ...)
   ```

6. **Anti-sous-tours** : position croissante le long de la tournée
   ```python
   model.Add(
       position[j, k] >= position[i, k] + 1 - self.n * (1 - x[i, j, k])
   )
   ```

7. **Contraintes de batterie** (VRP vert) : consommation et recharge
   ```python
   # consommation lors du trajet
   model.Add(batterie[j, k] <= batterie[i, k] - consommation_ij + ...)
   # recharge complète aux stations
   if j_est_station:
       model.Add(batterie[j, k] == batterie_max_k)
   ```

**Objectif** : minimiser la distance totale
```python
model.Minimize(sum(distance[i][j] * x[i, j, k] for i, j, k))
```

#### 3. Architecture asynchrone

Le système utilise des **threads séparés** pour la résolution afin de garder l'interface web responsive :

```python
def _resoudre_vrp_thread(...):
    """résout le VRP dans un thread séparé"""
    # création du modèle VRP
    vrp = VRPClassique(...) ou VRPVert(...)
    # résolution avec mises à jour progressives
    resultat = _resoudre_avec_progression(vrp, limite_temps, solution_id)
```

Les mises à jour progressives permettent de suivre l'évolution de la résolution en temps réel via l'API.

#### 4. Gestion des capacités et autonomies multiples

Le système supporte des capacités et autonomies différentes par véhicule :

```python
# capacités individuelles par véhicule
capacites_vehicules = [50, 75, 100]  # pour 3 véhicules

# autonomies individuelles par véhicule (VRP vert)
autonomies_vehicules = [30.0, 40.0, 50.0]  # en kilomètres
```

#### 5. Gestion du temps et des horaires

**Système de temps** :
- **Unité de temps** : 1 unité = 1 minute
- **Référence temporelle** : 0 unité = 8h00 du matin
- **Conversion distance-temps** : 1 km parcouru = 5 minutes (5 unités)
- **Temps de service** : 10 minutes (10 unités) par client par défaut

**Calcul des horaires d'arrivée** :
Les horaires d'arrivée sont calculés dans le frontend à partir des tournées retournées par le solveur :
- Départ du dépôt : toujours 8h00 (0 unité)
- Pour chaque nœud suivant : `temps_arrivée = temps_précédent + temps_service + distance × 5`
- Si arrivée avant la fenêtre temporelle : attente jusqu'au début de la fenêtre
- Les horaires sont affichés au format HH:MM

**Affichage des résultats** :
- **Horaires par livreur** : distance parcourue, heure de début (8h00), heure de fin de tournée, itinéraire complet avec horaires d'arrivée à chaque point
- **Horaires de livraison par client** : heure d'arrivée et véhicule responsable pour chaque client
- **Couleurs** : chaque livreur a une couleur unique (rouge, bleu, vert, etc.) visible à la fois sur la carte et dans les résultats

#### 6. Indexation spéciale pour VRP vert

Pour le VRP vert, les nœuds sont indexés de manière spéciale :
- Index 0 : dépôt
- Index 1..n : clients
- Index n+1..n+m : stations de recharge

Cette organisation permet de distinguer facilement les types de nœuds dans les contraintes.

### Complexité

- **Complexité théorique** : NP-difficile
- **Complexité pratique** : O($n! \cdot K$) dans le pire cas, mais les solveurs modernes utilisent des heuristiques efficaces

---

## 🔄 Explication rapide du flux de données

```
┌─────────────────┐
│  Interface Web  │
│   (index.html)  │
└────────┬────────┘
         │
         │ 1. Configuration du problème
         │    (clics sur carte, paramètres)
         ▼
┌─────────────────┐
│   Flask API     │
│   (app.py)      │
│  /api/solve     │
└────────┬────────┘
         │
         │ 2. Création d'un thread de résolution
         │
         ▼
┌─────────────────┐
│ Thread séparé   │
│ (asynchrone)    │
└────────┬────────┘
         │
         │ 3. Instanciation VRPClassique ou VRPVert
         │
         ▼
┌─────────────────┐
│  Backend VRP    │
│ vrp_classique.py│
│  vrp_vert.py    │
└────────┬────────┘
         │
         │ 4. Calcul matrice de distances (Haversine)
         │ 5. Création modèle CP-SAT
         │ 6. Définition variables et contraintes
         │
         ▼
┌─────────────────┐
│  OR-Tools       │
│  CP-SAT Solver  │
└────────┬────────┘
         │
         │ 7. Résolution (optimisation)
         │
         ▼
┌─────────────────┐
│ Extraction      │
│ des résultats   │
│ (tournées)      │
└────────┬────────┘
         │
         │ 8. Stockage dans solutions_en_cours
         │
         ▼
┌─────────────────┐
│  API Polling    │
│ /api/solution/  │
└────────┬────────┘
         │
         │ 9. Récupération par l'interface
         │
         ▼
┌─────────────────┐
│ Visualisation   │
│ sur carte       │
│ (Leaflet)       │
└─────────────────┘
```

### Étapes détaillées

1. **Interface utilisateur** : l'utilisateur clique sur la carte pour définir dépôt, clients et stations (si VRP vert), puis configure les paramètres.

2. **Requête API** : l'interface envoie une requête POST à `/api/solve` avec tous les paramètres du problème.

3. **Thread de résolution** : Flask crée un thread séparé pour éviter de bloquer l'interface pendant la résolution.

4. **Création du modèle** : selon le type (classique ou vert), instanciation de `VRPClassique` ou `VRPVert`.

5. **Calcul des distances** : calcul de la matrice de distances entre tous les points avec la formule de Haversine.

6. **Modélisation CP-SAT** : création des variables de décision et définition de toutes les contraintes.

7. **Résolution** : OR-Tools CP-SAT explore l'espace de recherche pour trouver une solution optimale ou réalisable.

8. **Mises à jour progressives** : pendant la résolution, des mises à jour sont envoyées à `solutions_en_cours` pour feedback temps réel.

9. **Polling** : l'interface interroge régulièrement `/api/solution/<id>` pour récupérer l'état de la résolution.

10. **Visualisation** : une fois la solution obtenue, les tournées sont affichées sur la carte Leaflet avec des couleurs différentes par véhicule.

11. **Calcul des horaires** : le frontend calcule les horaires d'arrivée réels à partir des distances Haversine, en respectant les contraintes temporelles (1 km = 5 min, 10 min de service par client).

12. **Affichage des résultats** : une fenêtre de résultats détaillée affiche pour chaque livreur sa distance, ses horaires de début/fin, son itinéraire complet, et un résumé des horaires de livraison par client.

---

## 🔮 Améliorations possibles

### Algorithmes et performances

1. **Heuristiques de construction** :
   - Implémentation d'heuristiques (nearest neighbor, Clark-Wright savings)
   - Utilisation comme solution initiale pour accélérer CP-SAT

2. **Algorithmes méta-heuristiques** :
   - Algorithmes génétiques pour grandes instances
   - Simulated annealing
   - Hybridation exact/heuristique

3. **Optimisations techniques** :
   - Parallélisation multi-thread pour plusieurs véhicules
   - Cache des matrices de distances
   - Pré-traitement pour éliminer les arcs impossibles
   - Réduction du problème (élimination de variables redondantes)

---

## 📁 Structure du projet

```
VRP-Alexis-Clement-Gregoire/
├── main.py                      # Point d'entrée principal
├── requirements.txt             # Dépendances Python
├── README.md                    # Documentation du projet
│
├── backend/                     # Logique de résolution VRP
│   ├── vrp_classique.py        # Implémentation VRP classique
│   └── vrp_vert.py             # Implémentation VRP vert (E-VRP)
│
└── frontend/                    # Interface web
    ├── app.py                   # Application Flask (API)
    ├── templates/
    │   └── index.html          # Interface web interactive
    └── static/
        └── images/             # Images et logos
```

### Description des modules

#### `main.py`
Script de démarrage qui :
- Vérifie les dépendances
- Lance l'application Flask
- Affiche les informations de démarrage

#### `backend/vrp_classique.py`
Classe `VRPClassique` qui implémente :
- Calcul de matrice de distances euclidiennes (Haversine)
- Modélisation CP-SAT avec variables de décision
- Contraintes de capacité, fenêtres temporelles, flux
- Extraction et formatage des solutions

**Points clés** :
- Variables booléennes `x[i,j,k]` : véhicule $k$ va de $i$ à $j$
- Variables entières pour position, temps, charge
- Contraintes de conservation de flux et élimination de sous-tours
- **Conversion distance-temps** : distances multipliées par 5 pour obtenir le temps de trajet (1 km = 5 min)
- **Temps de service** : 10 minutes (10 unités) par défaut pour chaque client

#### `backend/vrp_vert.py`
Classe `VRPVert` qui étend le VRP classique avec :
- Gestion des stations de recharge
- Variables de niveau de batterie
- Contraintes de consommation et recharge
- Suivi des stations visitées

**Extensions** :
- Indexation spéciale : dépôt (0), clients (1..n), stations (n+1..n+m)
- Contraintes de batterie avec recharge complète aux stations
- Temps de recharge intégré dans les fenêtres temporelles

#### `frontend/app.py`
Application Flask avec :
- Route principale `/` : rendu de l'interface
- API `/api/solve` : lancement de la résolution
- API `/api/solution/<id>` : récupération de l'état
- API `/api/solution/<id>/stream` : streaming Server-Sent Events

**Architecture asynchrone** :
- Résolution dans des threads séparés
- Mises à jour progressives pour feedback temps réel
- Gestion d'état avec dictionnaire global `solutions_en_cours`

#### `frontend/templates/index.html`
Interface web interactive avec :
- Carte Leaflet pour visualisation
- Gestion des événements de clic (dépôt, clients, stations)
- Communication AJAX avec le backend
- Affichage dynamique des tournées et statistiques
- **Configuration des fenêtres temporelles** : sélecteurs d'heures (8h-20h) et minutes (par tranches de 10) pour chaque client
- **Calcul des horaires d'arrivée** : fonction `calculerHorairesArrivee()` qui calcule les horaires réels à partir des distances Haversine
- **Affichage détaillé des résultats** :
  - Horaires par livreur avec distance, début/fin de tournée, itinéraire complet
  - Horaires de livraison par client
  - Bande colorée correspondant à la couleur du tracé sur la carte
  - Fenêtre de résultats réductible en bulle

---

## 📖 Références

### Documentation technique

- **OR-Tools Documentation** : https://developers.google.com/optimization
- **CP-SAT Solver** : https://developers.google.com/optimization/cp/cp_solver
- **Flask Documentation** : https://flask.palletsprojects.com/
- **Leaflet.js** : https://leafletjs.com/

### Littérature académique

- **Toth, P., & Vigo, D.** (2014). *Vehicle Routing: Problems, Methods, and Applications*. SIAM.
- **Perron, L., & Furnon, V.** (2019). *OR-Tools*. Google AI.

### Articles et ressources

- **VRP Variants** : https://en.wikipedia.org/wiki/Vehicle_routing_problem
- **E-VRP** : Schneider, M., Stenger, A., & Goeke, D. (2014). The Electric Vehicle-Routing Problem with Time Windows and Recharging Stations. *Transportation Science*, 48(4), 500-520.

### Formules mathématiques

- **Formule de Haversine** : https://en.wikipedia.org/wiki/Haversine_formula
- **Constraint Programming** : https://en.wikipedia.org/wiki/Constraint_programming
