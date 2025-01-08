import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
from scipy.optimize import curve_fit

# Définir la fonction logarithmique
def model(x, a, b):
    return a * np.log10(x) + b

# Connexion à la base de données
conn = mysql.connector.connect(host="192.168.1.20",
                               user="root",
                               password="root",
                               database="mesure_esp32")

cursor = conn.cursor()

# Récupération des données depuis la base de données
sql = "SELECT num_echantillon, valeur_Rssi FROM mesureESP32"
cursor.execute(sql)
results = cursor.fetchall()

distance = []
rssi = []

for row in results:
    distance.append(float(row[0]))  # num_echantillon comme approximation de la distance
    rssi.append(float(row[1]))

# Fermeture de la connexion
cursor.close()
conn.close()

# Utiliser curve_fit pour ajuster la fonction aux données
params, covariance = curve_fit(model, distance, rssi)

# Extraire les paramètres ajustés a et b
a, b = params
print(f'Paramètre a: {a}')
print(f'Paramètre b: {b}')

# Créer une plage plus dense de distances pour une courbe plus lisse
distance_fine = np.linspace(min(distance), max(distance), 500)

courbeEmpirique = model(distance_fine, *params)

# Créer un graphique avec 2 sous-graphiques côte à côte
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

axs[0].scatter(distance, rssi, s=10, c='red', label="Wifi distance RSSI")
axs[0].plot(distance_fine, courbeEmpirique, color='blue', label=f"Régression : RSSI = {a:.3f} * log10(dist) + {b:.3f}")
axs[0].grid()
axs[0].set_xlabel('Dist = fct(RSSI)', fontsize=10)
axs[0].set_ylabel("RSSI (dBm)", fontsize=10)
axs[0].set_xlabel("Distance (m)", fontsize=10)
axs[0].legend(fontsize=10)

axs[1].plot(courbeEmpirique, distance_fine, color='blue', label=f"Dist = 10^((RSSI - {b:.3f}) / {a:.3f})")
axs[1].grid()
axs[1].set_title('Dist = fct(RSSI)', fontsize=10)
axs[1].set_xlabel("RSSI (dBm)", fontsize=10)
axs[1].set_ylabel("Distance (m)", fontsize=10)
axs[1].legend(fontsize=10)

plt.tight_layout()
plt.show()
