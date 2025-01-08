import matplotlib.pyplot as plt
import matplotlib.patches as patches
import mysql.connector
import numpy as np

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
sql = "SELECT num_echantillon, valeur_Rssi FROM mesureESP32 ORDER BY num_echantillon LIMIT 3"
cursor.execute(sql)
results = cursor.fetchall()

# Traitement des données
rssi_values = [result[1] for result in results]  # Extraction des valeurs RSSI

print("Valeurs RSSI récupérées:", rssi_values)

# Calcul des rayons
def calculate_distance(rssi):
    return 10**((rssi-(-26.836)) / -23.994)

rayons = [calculate_distance(rssi) for rssi in rssi_values]

print("Rayons calculés:", rayons)

# Assurez-vous d'avoir 3 valeurs de rayon (une pour chaque borne)
rayonCIEL1 = rayons[0] if len(rayons) > 0 else 0
rayonCIEL2 = rayons[1] if len(rayons) > 1 else 0
rayonCIEL3 = rayons[2] if len(rayons) > 2 else 0

# Coordonnées des balises
points = [(0, 0, rayonCIEL1), (6, 5, rayonCIEL2), (18, 1, rayonCIEL3)]

fig, ax = plt.subplots(figsize=(12, 8))
# Dessin pièce
ax.add_patch(patches.Rectangle((0, 0), longueur, largeur, edgecolor='black', facecolor='lightgrey'))

# Placement des bornes Wifi
for borneNum, (x, y, rayon) in enumerate(points):
    print(f"Dessin de la borne {borneNum} à ({x}, {y}) avec rayon {rayon}")
    ax.plot(x, y, 'ro')  #en rouge
    ax.text(x + 0.2, y + 0.2, f'Borne {borneNum}', color='red', fontsize=8)
    
    if rayon > 0:
        circle = patches.Circle((x, y), rayon, edgecolor='blue', facecolor='none', linestyle='--')
        ax.add_patch(circle)

# Ajuster les axes pour bien voir le graphique
ax.set_xlim(-1, longueur + 1)
ax.set_ylim(-1, largeur + 1)
ax.set_aspect('equal')
ax.grid(True)

print(f"Limites du graphique : x de {ax.get_xlim()[0]} à {ax.get_xlim()[1]}, y de {ax.get_ylim()[0]} à {ax.get_ylim()[1]}")

# Ajouter des labels et un titre
plt.xlabel('Longueur (mètres)')
plt.ylabel('Largeur (mètres)')
plt.title('Simulation de la pièce')

# Afficher le graphique
plt.show()

# Fermer la connexion à la base de données
cursor.close()
conn.close()
