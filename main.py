"""
Script principal pour tester les différentes variantes du VRP.
"""

import sys
from vrp_classique import VRPClassique
from vrp_vert import VRPVert
from visualisation import visualiser_solution_vrp_classique, visualiser_solution_vrp_vert


def exemple_complet():
    """exemple complet comparant VRP classique et VRP vert"""
    
    print("=" * 60)
    print("Comparaison VRP Classique vs VRP Vert")
    print("=" * 60)
    
    # données communes
    depot = (48.8566, 2.3522)  # paris
    
    clients = [
        (48.8606, 2.3376),
        (48.8530, 2.3499),
        (48.8550, 2.3700),
        (48.8500, 2.3400),
        (48.8580, 2.3600),
        (48.8520, 2.3550),
    ]
    
    demandes = [10, 15, 20, 12, 18, 14]
    capacite = 50
    fenetres = [(0, 150), (20, 170), (40, 190), (60, 210), (80, 230), (100, 250)]
    temps_service = [10, 15, 20, 12, 18, 14]
    
    # === VRP CLASSIQUE ===
    print("\n1. Résolution VRP Classique...")
    vrp_classique = VRPClassique(
        depot=depot,
        clients=clients,
        demandes=demandes,
        capacite_vehicule=capacite,
        fenetres_temps=fenetres,
        temps_service=temps_service,
        nombre_vehicules=2
    )
    
    resultat_classique = vrp_classique.resoudre(limite_temps=30)
    
    print(f"   Statut: {resultat_classique['statut']}")
    print(f"   Distance totale: {resultat_classique['distance_totale']:.2f}")
    print(f"   Véhicules utilisés: {resultat_classique['nombre_vehicules_utilises']}")
    
    visualiser_solution_vrp_classique(
        depot, clients, resultat_classique, 'resultat_vrp_classique.html'
    )
    print("   → Visualisation: resultat_vrp_classique.html")
    
    # === VRP VERT ===
    print("\n2. Résolution VRP Vert (véhicules électriques)...")
    
    stations = [
        (48.8520, 2.3450),
        (48.8570, 2.3650),
    ]
    
    vrp_vert = VRPVert(
        depot=depot,
        clients=clients,
        stations_recharge=stations,
        demandes=demandes,
        capacite_vehicule=capacite,
        autonomie_max=80.0,
        consommation=1.0,
        temps_recharge=30,
        fenetres_temps=fenetres,
        temps_service=temps_service,
        nombre_vehicules=2
    )
    
    resultat_vert = vrp_vert.resoudre(limite_temps=60)
    
    print(f"   Statut: {resultat_vert['statut']}")
    print(f"   Distance totale: {resultat_vert['distance_totale']:.2f}")
    print(f"   Véhicules utilisés: {resultat_vert['nombre_vehicules_utilises']}")
    print(f"   Stations visitées: {resultat_vert['stations_visitees']}")
    
    visualiser_solution_vrp_vert(
        depot, clients, stations, resultat_vert, 'resultat_vrp_vert.html'
    )
    print("   → Visualisation: resultat_vrp_vert.html")
    
    # === COMPARAISON ===
    print("\n" + "=" * 60)
    print("Comparaison des résultats:")
    print("=" * 60)
    print(f"VRP Classique - Distance: {resultat_classique['distance_totale']:.2f}")
    print(f"VRP Vert      - Distance: {resultat_vert['distance_totale']:.2f}")
    
    if resultat_vert['distance_totale'] > resultat_classique['distance_totale']:
        diff = resultat_vert['distance_totale'] - resultat_classique['distance_totale']
        print(f"\nLe VRP vert parcourt {diff:.2f} unités de plus")
        print("(contrainte d'autonomie nécessite des détours par les stations)")
    else:
        print("\nLes deux solutions ont des distances similaires")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("Usage: python main.py")
        print("\nExécute une comparaison entre VRP classique et VRP vert")
        sys.exit(0)
    
    exemple_complet()

