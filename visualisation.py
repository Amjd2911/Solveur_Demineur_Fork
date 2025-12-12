"""
Module de visualisation des tournées VRP avec Folium.
Permet de visualiser les tournées sur une carte interactive.
"""

import folium
from folium import plugins
from typing import List, Tuple, Dict
import numpy as np


class VisualiseurVRP:
    """classe pour visualiser les solutions VRP sur une carte"""
    
    def __init__(self, depot: Tuple[float, float], clients: List[Tuple[float, float]]):
        """
        Initialise le visualiseur.
        
        Args:
            depot: Coordonnées (lat, lon) du dépôt
            clients: Liste des coordonnées (lat, lon) des clients
        """
        self.depot = depot
        self.clients = clients
        
        # centre de la carte au dépôt
        self.carte = folium.Map(
            location=depot,
            zoom_start=12,
            tiles='OpenStreetMap'
        )
    
    def ajouter_depot(self, couleur: str = 'red', taille: int = 15):
        """ajoute le dépôt sur la carte"""
        folium.Marker(
            location=self.depot,
            popup='Dépôt',
            icon=folium.Icon(color=couleur, icon='home', prefix='fa'),
            tooltip='Dépôt'
        ).add_to(self.carte)
    
    def ajouter_clients(self, couleur: str = 'blue', taille: int = 10):
        """ajoute tous les clients sur la carte"""
        for i, client in enumerate(self.clients):
            folium.CircleMarker(
                location=client,
                radius=taille,
                popup=f'Client {i+1}',
                color=couleur,
                fill=True,
                fillColor=couleur,
                tooltip=f'Client {i+1}'
            ).add_to(self.carte)
    
    def ajouter_stations_recharge(self, stations: List[Tuple[float, float]], 
                                   couleur: str = 'green', taille: int = 12):
        """ajoute les stations de recharge sur la carte"""
        for i, station in enumerate(stations):
            folium.Marker(
                location=station,
                popup=f'Station {i+1}',
                icon=folium.Icon(color=couleur, icon='bolt', prefix='fa'),
                tooltip=f'Station de recharge {i+1}'
            ).add_to(self.carte)
    
    def ajouter_tournee(self, tournee: List[int], couleur: str = 'blue', 
                        epaisseur: int = 3, label: str = ''):
        """
        Ajoute une tournée sur la carte.
        
        Args:
            tournee: Liste d'indices représentant l'ordre de visite
                    (0 = dépôt, 1+ = clients)
            couleur: Couleur de la ligne
            epaisseur: Épaisseur de la ligne
            label: Label pour la tournée
        """
        points = []
        
        # convertir les indices en coordonnées
        for idx in tournee:
            if idx == 0:
                points.append(self.depot)
            else:
                # idx-1 car les clients commencent à l'index 1
                if idx - 1 < len(self.clients):
                    points.append(self.clients[idx - 1])
        
        # tracer la ligne
        if len(points) > 1:
            folium.PolyLine(
                points,
                color=couleur,
                weight=epaisseur,
                opacity=0.7,
                popup=label,
                tooltip=label
            ).add_to(self.carte)
    
    def ajouter_tournee_vert(self, tournee: List[int], 
                            stations_recharge: List[Tuple[float, float]],
                            n_clients: int, couleur: str = 'green',
                            epaisseur: int = 3, label: str = ''):
        """
        Ajoute une tournée E-VRP avec stations de recharge.
        
        Args:
            tournee: Liste d'indices (0=dépôt, 1..n=clients, n+1..=stations)
            stations_recharge: Liste des coordonnées des stations
            n_clients: Nombre de clients
            couleur: Couleur de la ligne
            epaisseur: Épaisseur de la ligne
            label: Label pour la tournée
        """
        points = []
        
        for idx in tournee:
            if idx == 0:
                points.append(self.depot)
            elif idx <= n_clients:
                # c'est un client
                points.append(self.clients[idx - 1])
            else:
                # c'est une station de recharge
                station_idx = idx - 1 - n_clients
                if station_idx < len(stations_recharge):
                    points.append(stations_recharge[station_idx])
        
        if len(points) > 1:
            folium.PolyLine(
                points,
                color=couleur,
                weight=epaisseur,
                opacity=0.7,
                popup=label,
                tooltip=label
            ).add_to(self.carte)
    
    def sauvegarder(self, nom_fichier: str = 'tournees.html'):
        """sauvegarde la carte dans un fichier HTML"""
        self.carte.save(nom_fichier)
        print(f"Carte sauvegardée dans {nom_fichier}")
    
    def afficher(self):
        """retourne l'objet carte pour affichage"""
        return self.carte


def visualiser_solution_vrp_classique(
    depot: Tuple[float, float],
    clients: List[Tuple[float, float]],
    resultat: Dict,
    nom_fichier: str = 'tournees_classiques.html'
):
    """
    Visualise une solution VRP classique.
    
    Args:
        depot: Coordonnées du dépôt
        clients: Liste des coordonnées des clients
        resultat: Dictionnaire de résultat de VRPClassique.resoudre()
        nom_fichier: Nom du fichier de sortie
    """
    visu = VisualiseurVRP(depot, clients)
    visu.ajouter_depot()
    visu.ajouter_clients()
    
    couleurs = ['blue', 'red', 'green', 'purple', 'orange', 'darkred', 
                'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue',
                'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen',
                'gray', 'black', 'lightgray']
    
    for i, tournee in enumerate(resultat['tournees']):
        couleur = couleurs[i % len(couleurs)]
        visu.ajouter_tournee(
            tournee, 
            couleur=couleur,
            label=f'Véhicule {i+1}'
        )
    
    visu.sauvegarder(nom_fichier)


def visualiser_solution_vrp_vert(
    depot: Tuple[float, float],
    clients: List[Tuple[float, float]],
    stations_recharge: List[Tuple[float, float]],
    resultat: Dict,
    nom_fichier: str = 'tournees_vertes.html'
):
    """
    Visualise une solution E-VRP.
    
    Args:
        depot: Coordonnées du dépôt
        clients: Liste des coordonnées des clients
        stations_recharge: Liste des coordonnées des stations
        resultat: Dictionnaire de résultat de VRPVert.resoudre()
        nom_fichier: Nom du fichier de sortie
    """
    visu = VisualiseurVRP(depot, clients)
    visu.ajouter_depot()
    visu.ajouter_clients()
    visu.ajouter_stations_recharge(stations_recharge)
    
    couleurs = ['green', 'darkgreen', 'lightgreen', 'blue', 'red', 'purple']
    
    n_clients = len(clients)
    
    for i, tournee in enumerate(resultat['tournees']):
        couleur = couleurs[i % len(couleurs)]
        visu.ajouter_tournee_vert(
            tournee,
            stations_recharge,
            n_clients,
            couleur=couleur,
            label=f'Véhicule électrique {i+1}'
        )
    
    visu.sauvegarder(nom_fichier)

