"""
Exemple d'utilisation du VRP vert (véhicules électriques).
"""

from vrp_vert import VRPVert
from visualisation import visualiser_solution_vrp_vert
import random


def exemple_simple_vert():
    """exemple simple avec véhicules électriques"""
    
    # dépôt
    depot = (48.8566, 2.3522)  # paris
    
    # clients
    clients = [
        (48.8606, 2.3376),
        (48.8530, 2.3499),
        (48.8550, 2.3700),
        (48.8500, 2.3400),
        (48.8580, 2.3600),
    ]
    
    # stations de recharge
    stations = [
        (48.8520, 2.3450),
        (48.8570, 2.3650),
    ]
    
    # demandes
    demandes = [10, 15, 20, 12, 18]
    
    # paramètres véhicule électrique
    capacite = 50
    autonomie_max = 100.0  # unités de distance
    consommation = 1.0  # consommation par unité de distance
    temps_recharge = 30  # unités de temps
    
    # fenêtres temporelles
    fenetres = [
        (0, 200),
        (20, 220),
        (40, 240),
        (60, 260),
        (80, 280),
    ]
    
    # temps de service
    temps_service = [10, 15, 20, 12, 18]
    
    # nombre de véhicules
    nb_vehicules = 2
    
    # création et résolution
    vrp = VRPVert(
        depot=depot,
        clients=clients,
        stations_recharge=stations,
        demandes=demandes,
        capacite_vehicule=capacite,
        autonomie_max=autonomie_max,
        consommation=consommation,
        temps_recharge=temps_recharge,
        fenetres_temps=fenetres,
        temps_service=temps_service,
        nombre_vehicules=nb_vehicules
    )
    
    print("Résolution du VRP vert (véhicules électriques)...")
    resultat = vrp.resoudre(limite_temps=60)
    
    # affichage des résultats
    print(f"\nStatut: {resultat['statut']}")
    print(f"Distance totale: {resultat['distance_totale']:.2f}")
    print(f"Nombre de véhicules utilisés: {resultat['nombre_vehicules_utilises']}")
    print("\nTournées:")
    for i, tournee in enumerate(resultat['tournees']):
        print(f"  Véhicule {i+1}: {tournee}")
        if i < len(resultat['stations_visitees']):
            print(f"    Stations visitées: {resultat['stations_visitees'][i]}")
    
    # visualisation
    visualiser_solution_vrp_vert(
        depot, clients, stations, resultat, 'exemple_vrp_vert.html'
    )
    print("\nVisualisation sauvegardée dans 'exemple_vrp_vert.html'")


def exemple_aleatoire_vert(n_clients=8, n_stations=3):
    """exemple avec des données générées aléatoirement"""
    
    depot = (48.8566, 2.3522)
    
    # génération aléatoire
    random.seed(42)
    clients = []
    for _ in range(n_clients):
        lat = depot[0] + random.uniform(-0.05, 0.05)
        lon = depot[1] + random.uniform(-0.05, 0.05)
        clients.append((lat, lon))
    
    # stations de recharge
    stations = []
    for _ in range(n_stations):
        lat = depot[0] + random.uniform(-0.05, 0.05)
        lon = depot[1] + random.uniform(-0.05, 0.05)
        stations.append((lat, lon))
    
    # demandes
    demandes = [random.randint(5, 25) for _ in range(n_clients)]
    
    # paramètres
    capacite = 50
    autonomie_max = 80.0
    consommation = 1.0
    temps_recharge = 30
    
    # fenêtres temporelles
    fenetres = []
    for i in range(n_clients):
        debut = i * 25
        fin = debut + 150
        fenetres.append((debut, fin))
    
    # temps de service
    temps_service = [random.randint(5, 20) for _ in range(n_clients)]
    
    # nombre de véhicules
    nb_vehicules = 2
    
    # résolution
    vrp = VRPVert(
        depot=depot,
        clients=clients,
        stations_recharge=stations,
        demandes=demandes,
        capacite_vehicule=capacite,
        autonomie_max=autonomie_max,
        consommation=consommation,
        temps_recharge=temps_recharge,
        fenetres_temps=fenetres,
        temps_service=temps_service,
        nombre_vehicules=nb_vehicules
    )
    
    print(f"Résolution du VRP vert avec {n_clients} clients et {n_stations} stations...")
    resultat = vrp.resoudre(limite_temps=90)
    
    print(f"\nStatut: {resultat['statut']}")
    print(f"Distance totale: {resultat['distance_totale']:.2f}")
    print(f"Nombre de véhicules utilisés: {resultat['nombre_vehicules_utilises']}")
    
    # visualisation
    visualiser_solution_vrp_vert(
        depot, clients, stations, resultat, 'exemple_vrp_vert_aleatoire.html'
    )
    print("Visualisation sauvegardée dans 'exemple_vrp_vert_aleatoire.html'")


if __name__ == '__main__':
    print("=== Exemple simple VRP vert ===")
    exemple_simple_vert()
    
    print("\n=== Exemple aléatoire VRP vert ===")
    exemple_aleatoire_vert(8, 3)

