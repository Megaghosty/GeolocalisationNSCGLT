import matplotlib.pyplot as plt
import matplotlib.patches as patches
import mysql.connector
import numpy as np
from scipy.optimize import minimize

# Dimensions de la pièce
longueur = 20  # en mètres
largeur = 6    # en mètres

# Connexion à la base de données
conn = mysql.connector.connect(host="192.168.1.20",
                               user="root",
                               password="root",
                               database="mesure_esp32")

cursor = conn.cursor()

# Récupération des données depuis la base de données
sql = "SELECT num_echantillon, valeur_Rssi FROM mesureESP32 ORDER BY num_echantillon"
cursor.execute(sql)
results = cursor.fetchall()

# Traitement des données
rssi_values = [result[1] for result in results]  # Extraction des valeurs RSSI

# Affichage des valeurs pour débogage
print("Valeurs RSSI complètes:", rssi_values)
print("Nombre total de valeurs:", len(rssi_values))

# Fonction pour calculer la distance
def calculate_distance(rssi):
    return 10**((rssi - (-32)) / -23.994)

# Traitement des données par groupe de 20 pour chaque borne
rayons = []
for i in range(0, len(rssi_values), 20):
    borne_rssi = rssi_values[i:i + 20]
    if len(borne_rssi) == 20:  # Assurez-vous d'avoir exactement 20 échantillons
        avg_rssi = sum(borne_rssi) / len(borne_rssi)
        rayon = calculate_distance(avg_rssi)
        rayons.append(rayon)
    else:
        rayons.append(0)  # Ajouter 0 si pas assez de données

print("Rayons calculés pour chaque borne:", rayons)

# Fonction pour calculer la position estimée par trilatération
def trilaterate(points):
    # Filtrer les points avec un rayon > 0
    valid_points = [p for p in points if p[2] > 0]
    
    if len(valid_points) < 3:
        print("Pas assez de points pour trilatérer")
        return [longueur / 2, largeur / 2]  # Position par défaut au centre
    
    def error(x, points):
        return sum([(np.sqrt((x[0] - p[0]) ** 2 + (x[1] - p[1]) ** 2) - p[2]) ** 2 for p in points])
    
    initial_guess = [np.mean([p[0] for p in valid_points]), np.mean([p[1] for p in valid_points])]
    result = minimize(error, initial_guess, args=(valid_points,), method='L-BFGS-B',
                      bounds=((0, longueur), (0, largeur)))
    return result.x

# Assurez-vous d'avoir 3 valeurs de rayon (une pour chaque borne)
rayonCIEL1 = rayons[0] if len(rayons) > 0 else 0
rayonCIEL2 = rayons[1] if len(rayons) > 1 else 0
rayonCIEL3 = rayons[2] if len(rayons) > 2 else 0

# Coordonnées des balises
points = [(0, 0, rayonCIEL1), (10, 5, rayonCIEL2), (18, 1, rayonCIEL3)]

# Calculer la position estimée
estimated_position = trilaterate(points)

fig, ax = plt.subplots(figsize=(12, 8))
# Dessin pièce
ax.add_patch(patches.Rectangle((0, 0), longueur, largeur, edgecolor='black', facecolor='lightgrey'))

# Placement des bornes Wifi et cercles
for borneNum, (x, y, rayon) in enumerate(points):
    print(f"Dessin de la borne {borneNum} à ({x}, {y}) avec rayon {rayon}")
    ax.plot(x, y, 'ro')  # en rouge
    ax.text(x + 0.2, y + 0.2, f'Borne {borneNum + 1}', color='red', fontsize=8)
    
    if rayon > 0:
        circle = patches.Circle((x, y), rayon, edgecolor='blue', facecolor='none', linestyle='--')
        ax.add_patch(circle)

# Afficher la position estimée
ax.plot(estimated_position[0], estimated_position[1], 'go', markersize=10)  # Point vert
ax.text(estimated_position[0] + 0.2, estimated_position[1] + 0.2, 'Position estimée', color='green', fontsize=10)

# Ajuster les axes pour bien voir le graphique
ax.set_xlim(-1, longueur + 1)
ax.set_ylim(-1, largeur + 1)
ax.set_aspect('equal')
ax.grid(True)

# Ajouter des labels et un titre
plt.xlabel('Longueur (mètres)')
plt.ylabel('Largeur (mètres)')
plt.title('Simulation de la pièce avec position estimée')

# Afficher le graphique
plt.show()

# Fermer la connexion à la base de données
cursor.close()
conn.close()

