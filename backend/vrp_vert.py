"""
Module pour résoudre le problème de tournées de véhicules électriques (E-VRP)
avec contraintes d'autonomie et de recharge.
Utilise OR-Tools CP-SAT pour la résolution.
"""

from ortools.sat.python import cp_model
import numpy as np
from typing import List, Tuple, Dict, Optional


class VRPVert:
    """
    Classe pour résoudre le VRP "vert" avec véhicules électriques :
    - Contraintes de capacité
    - Contraintes d'autonomie (batterie)
    - Stations de recharge
    - Fenêtres temporelles
    - Minimisation de l'empreinte carbone (distance)
    """
    
    def __init__(
        self,
        depot: Tuple[float, float],
        clients: List[Tuple[float, float]],
        stations_recharge: List[Tuple[float, float]],
        demandes: List[int],
        capacite_vehicule: int,
        autonomie_max: float,
        consommation: float,  # consommation par unité de distance
        temps_recharge: int = 30,  # temps de recharge en unités de temps
        fenetres_temps: Optional[List[Tuple[int, int]]] = None,
        temps_service: Optional[List[int]] = None,
        nombre_vehicules: int = 1
    ):
        """
        Initialise le problème E-VRP.
        
        Args:
            depot: Coordonnées (x, y) du dépôt
            clients: Liste des coordonnées (x, y) des clients
            stations_recharge: Liste des coordonnées des stations de recharge
            demandes: Liste des demandes de chaque client
            capacite_vehicule: Capacité maximale d'un véhicule
            autonomie_max: Autonomie maximale de la batterie
            consommation: Consommation d'énergie par unité de distance
            temps_recharge: Temps nécessaire pour recharger complètement
            fenetres_temps: Liste de (début, fin) pour chaque client
            temps_service: Temps de service à chaque client
            nombre_vehicules: Nombre de véhicules disponibles
        """
        self.depot = depot
        self.clients = clients
        self.stations_recharge = stations_recharge
        self.demandes = demandes
        self.capacite_vehicule = capacite_vehicule
        self.autonomie_max = autonomie_max
        self.consommation = consommation
        self.temps_recharge = temps_recharge
        self.fenetres_temps = fenetres_temps or [(0, 10000)] * len(clients)
        self.temps_service = temps_service or [0] * len(clients)
        self.nombre_vehicules = nombre_vehicules
        
        # calcul des distances
        self.distances = self._calculer_distances()
        
        # indexation : 0 = dépôt, 1..n = clients, n+1..n+m = stations
        self.n_clients = len(clients)
        self.n_stations = len(stations_recharge)
        self.n_total = 1 + self.n_clients + self.n_stations
        
    def _calculer_distances(self) -> np.ndarray:
        """calcule la matrice des distances entre tous les points"""
        points = [self.depot] + self.clients + self.stations_recharge
        n = len(points)
        distances = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    dx = points[i][0] - points[j][0]
                    dy = points[i][1] - points[j][1]
                    distances[i][j] = np.sqrt(dx**2 + dy**2)
        
        return distances
    
    def _get_index_client(self, idx: int) -> int:
        """retourne l'index dans la matrice de distance pour un client"""
        return idx + 1  # 0 = dépôt, 1..n = clients
    
    def _get_index_station(self, idx: int) -> int:
        """retourne l'index dans la matrice de distance pour une station"""
        return 1 + self.n_clients + idx
    
    def resoudre(self, limite_temps: int = 60) -> Dict:
        """
        Résout le problème E-VRP avec CP-SAT.
        
        Args:
            limite_temps: Temps limite de résolution en secondes
            
        Returns:
            Dictionnaire contenant les tournées, distance totale, et statut
        """
        model = cp_model.CpModel()
        
        # variables de décision
        # x[i][j][k] = 1 si le véhicule k va de i à j
        x = {}
        for k in range(self.nombre_vehicules):
            for i in range(self.n_total):
                for j in range(self.n_total):
                    if i != j:
                        x[i, j, k] = model.NewBoolVar(f'x_{i}_{j}_{k}')
        
        # variables pour l'ordre de visite
        position = {}
        for k in range(self.nombre_vehicules):
            for i in range(self.n_total):
                position[i, k] = model.NewIntVar(0, self.n_total, f'pos_{i}_{k}')
        
        # variables pour le temps d'arrivée
        temps_arrivee = {}
        for k in range(self.nombre_vehicules):
            for i in range(self.n_total):
                temps_arrivee[i, k] = model.NewIntVar(0, 10000, f'time_{i}_{k}')
        
        # variables pour la charge du véhicule
        charge = {}
        for k in range(self.nombre_vehicules):
            for i in range(self.n_total):
                charge[i, k] = model.NewIntVar(0, self.capacite_vehicule, f'load_{i}_{k}')
        
        # variables pour le niveau de batterie (0 à autonomie_max)
        batterie = {}
        for k in range(self.nombre_vehicules):
            for i in range(self.n_total):
                batterie[i, k] = model.NewIntVar(
                    0, int(self.autonomie_max * 100), f'battery_{i}_{k}'
                )
        
        # contraintes : chaque client visité exactement une fois
        for j in range(1, 1 + self.n_clients):  # indices des clients
            model.Add(
                sum(x[i, j, k] for i in range(self.n_total) 
                    for k in range(self.nombre_vehicules) if i != j) == 1
            )
        
        # contraintes : chaque véhicule part du dépôt
        for k in range(self.nombre_vehicules):
            model.Add(sum(x[0, j, k] for j in range(1, self.n_total)) <= 1)
            model.Add(sum(x[i, 0, k] for i in range(1, self.n_total)) <= 1)
        
        # contraintes : conservation de flux
        for k in range(self.nombre_vehicules):
            for j in range(self.n_total):
                model.Add(
                    sum(x[i, j, k] for i in range(self.n_total) if i != j) ==
                    sum(x[j, i, k] for i in range(self.n_total) if i != j)
                )
        
        # contraintes : capacité
        for k in range(self.nombre_vehicules):
            model.Add(charge[0, k] == 0)  # départ avec charge vide
            
            for j in range(1, 1 + self.n_clients):  # pour chaque client
                demande_j = self.demandes[j-1]
                for i in range(self.n_total):
                    if i != j:
                        model.Add(
                            charge[j, k] >= charge[i, k] + demande_j - 
                            self.capacite_vehicule * (1 - x[i, j, k])
                        )
                        model.Add(
                            charge[j, k] <= charge[i, k] + demande_j + 
                            self.capacite_vehicule * (1 - x[i, j, k])
                        )
        
        # contraintes : batterie et autonomie
        batterie_max = int(self.autonomie_max * 100)
        
        for k in range(self.nombre_vehicules):
            # départ du dépôt avec batterie pleine
            model.Add(batterie[0, k] == batterie_max)
            
            for j in range(1, self.n_total):
                for i in range(self.n_total):
                    if i != j:
                        dist = int(self.distances[i][j] * 100)
                        consommation_ij = int(dist * self.consommation)
                        
                        # vérifier si i ou j sont des stations
                        i_est_station = (i >= 1 + self.n_clients)
                        j_est_station = (j >= 1 + self.n_clients)
                        
                        if j_est_station:
                            # si on arrive à une station, batterie = plein après recharge
                            model.Add(
                                batterie[j, k] >= batterie_max - 
                                batterie_max * (1 - x[i, j, k])
                            )
                            model.Add(batterie[j, k] <= batterie_max)
                        elif i_est_station:
                            # si on quitte une station, batterie de départ = plein
                            model.Add(
                                batterie[j, k] <= batterie_max - consommation_ij + 
                                batterie_max * (1 - x[i, j, k])
                            )
                            model.Add(
                                batterie[j, k] >= batterie_max - consommation_ij - 
                                batterie_max * (1 - x[i, j, k])
                            )
                        else:
                            # trajet normal entre dépôt/clients
                            model.Add(
                                batterie[j, k] <= batterie[i, k] - consommation_ij + 
                                batterie_max * (1 - x[i, j, k])
                            )
                            model.Add(
                                batterie[j, k] >= batterie[i, k] - consommation_ij - 
                                batterie_max * (1 - x[i, j, k])
                            )
                
                # contrainte : batterie ne peut pas être négative
                model.Add(batterie[j, k] >= 0)
        
        # contraintes : fenêtres temporelles
        for k in range(self.nombre_vehicules):
            model.Add(temps_arrivee[0, k] == 0)
            
            for j in range(1, 1 + self.n_clients):  # pour les clients
                debut, fin = self.fenetres_temps[j-1]
                model.Add(temps_arrivee[j, k] >= debut)
                model.Add(temps_arrivee[j, k] <= fin)
                
                for i in range(self.n_total):
                    if i != j:
                        dist = int(self.distances[i][j])
                        temps_trajet = dist
                        
                        # temps de service au nœud de départ i
                        if i == 0:
                            temps_serv = 0  # dépôt
                        elif i <= self.n_clients:
                            temps_serv = self.temps_service[i-1]  # client
                        else:
                            temps_serv = 0  # station (pas de service, juste recharge)
                        
                        # si on arrive à une station, ajouter temps de recharge
                        if j >= 1 + self.n_clients:
                            temps_serv = self.temps_recharge
                        
                        model.Add(
                            temps_arrivee[j, k] >= temps_arrivee[i, k] + 
                            temps_serv + temps_trajet - 
                            10000 * (1 - x[i, j, k])
                        )
        
        # contraintes : position dans la tournée (éviter sous-tours)
        for k in range(self.nombre_vehicules):
            model.Add(position[0, k] == 0)
            
            for i in range(1, self.n_total):
                for j in range(1, self.n_total):
                    if i != j:
                        model.Add(
                            position[j, k] >= position[i, k] + 1 - 
                            self.n_total * (1 - x[i, j, k])
                        )
        
        # objectif : minimiser la distance totale (empreinte carbone)
        objectif = []
        for k in range(self.nombre_vehicules):
            for i in range(self.n_total):
                for j in range(self.n_total):
                    if i != j:
                        dist = int(self.distances[i][j] * 100)
                        objectif.append(dist * x[i, j, k])
        
        model.Minimize(sum(objectif))
        
        # résolution
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = limite_temps
        status = solver.Solve(model)
        
        # extraction des résultats
        tournees = []
        distance_totale = 0
        stations_visitees = []
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            for k in range(self.nombre_vehicules):
                tournee = [0]  # commence au dépôt
                current = 0
                distance_vehicule = 0
                stations_k = []
                
                while True:
                    trouve = False
                    for j in range(self.n_total):
                        if j != current and solver.Value(x[current, j, k]) == 1:
                            tournee.append(j)
                            distance_vehicule += self.distances[current][j]
                            
                            # vérifier si c'est une station
                            if j >= 1 + self.n_clients:
                                stations_k.append(j - 1 - self.n_clients)
                            
                            current = j
                            trouve = True
                            break
                    
                    if not trouve or current == 0:
                        break
                
                if len(tournee) > 1:
                    tournees.append(tournee)
                    distance_totale += distance_vehicule
                    stations_visitees.append(stations_k)
        
        return {
            'statut': 'optimal' if status == cp_model.OPTIMAL else 'feasible' if status == cp_model.FEASIBLE else 'infeasible',
            'tournees': tournees,
            'distance_totale': distance_totale,
            'nombre_vehicules_utilises': len(tournees),
            'stations_visitees': stations_visitees
        }

