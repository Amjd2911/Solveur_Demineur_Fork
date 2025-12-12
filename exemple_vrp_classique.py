"""
Exemple d'utilisation du VRP classique.
"""

from vrp_classique import VRPClassique
from visualisation import visualiser_solution_vrp_classique
import random


def exemple_simple():
    """exemple simple avec quelques clients"""
    
    # dépôt (coordonnées)
    depot = (48.8566, 2.3522)  # paris
    
    # clients (coordonnées lat, lon)
    clients = [
        (48.8606, 2.3376),  # client 1
        (48.8530, 2.3499),  # client 2
        (48.8550, 2.3700),  # client 3
        (48.8500, 2.3400),  # client 4
        (48.8580, 2.3600),  # client 5
    ]
    
    # demandes de chaque client
    demandes = [10, 15, 20, 12, 18]
    
    # capacité d'un véhicule
    capacite = 50
    
    # fenêtres temporelles (début, fin) pour chaque client
    fenetres = [
        (0, 100),   # client 1
        (20, 120),  # client 2
        (40, 140),  # client 3
        (60, 160),  # client 4
        (80, 180),  # client 5
    ]
    
    # temps de service à chaque client
    temps_service = [10, 15, 20, 12, 18]
    
    # nombre de véhicules disponibles
    nb_vehicules = 2
    
    # création et résolution du problème
    vrp = VRPClassique(
        depot=depot,
        clients=clients,
        demandes=demandes,
        capacite_vehicule=capacite,
        fenetres_temps=fenetres,
        temps_service=temps_service,
        nombre_vehicules=nb_vehicules
    )
    
    print("Résolution du VRP classique...")
    resultat = vrp.resoudre(limite_temps=30)
    
    # affichage des résultats
    print(f"\nStatut: {resultat['statut']}")
    print(f"Distance totale: {resultat['distance_totale']:.2f}")
    print(f"Nombre de véhicules utilisés: {resultat['nombre_vehicules_utilises']}")
    print("\nTournées:")
    for i, tournee in enumerate(resultat['tournees']):
        print(f"  Véhicule {i+1}: {tournee}")
    
    # visualisation
    visualiser_solution_vrp_classique(
        depot, clients, resultat, 'exemple_vrp_classique.html'
    )
    print("\nVisualisation sauvegardée dans 'exemple_vrp_classique.html'")


def exemple_aleatoire(n_clients=10):
    """exemple avec des clients générés aléatoirement"""
    
    # zone autour de paris
    depot = (48.8566, 2.3522)
    
    # génération aléatoire de clients
    random.seed(42)
    clients = []
    for _ in range(n_clients):
        lat = depot[0] + random.uniform(-0.05, 0.05)
        lon = depot[1] + random.uniform(-0.05, 0.05)
        clients.append((lat, lon))
    
    # demandes aléatoires
    demandes = [random.randint(5, 25) for _ in range(n_clients)]
    
    # capacité
    capacite = 50
    
    # fenêtres temporelles
    fenetres = []
    for i in range(n_clients):
        debut = i * 20
        fin = debut + 100
        fenetres.append((debut, fin))
    
    # temps de service
    temps_service = [random.randint(5, 20) for _ in range(n_clients)]
    
    # nombre de véhicules
    nb_vehicules = 3
    
    # résolution
    vrp = VRPClassique(
        depot=depot,
        clients=clients,
        demandes=demandes,
        capacite_vehicule=capacite,
        fenetres_temps=fenetres,
        temps_service=temps_service,
        nombre_vehicules=nb_vehicules
    )
    
    print(f"Résolution du VRP avec {n_clients} clients...")
    resultat = vrp.resoudre(limite_temps=60)
    
    print(f"\nStatut: {resultat['statut']}")
    print(f"Distance totale: {resultat['distance_totale']:.2f}")
    print(f"Nombre de véhicules utilisés: {resultat['nombre_vehicules_utilises']}")
    
    # visualisation
    visualiser_solution_vrp_classique(
        depot, clients, resultat, 'exemple_vrp_aleatoire.html'
    )
    print("Visualisation sauvegardée dans 'exemple_vrp_aleatoire.html'")


if __name__ == '__main__':
    print("=== Exemple simple ===")
    exemple_simple()
    
    print("\n=== Exemple aléatoire ===")
    exemple_aleatoire(10)

