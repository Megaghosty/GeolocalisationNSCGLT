import csv
import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
from statsmodels.regression.quantile_regression import QuantReg
from scipy.optimize import curve_fit  
from scipy.stats import linregress  



conn = mysql.connector.connect(host="192.168.1.___",
                                      user="root",
                                      password="root",
                                      database="_______" ) #geoLocoWifi")

cursor = conn.cursor()

# Définir la fonction logarithmique
def model(x, a, b):
    return a * np.log10(x) + b

res=[]
distance=[]
rssi =[]


#ATTENTION PEUT CHANGER EN FONCTION DU FORMAT DE VOS DONNEES
with open('echDistance.csv', newline='') as csvfile: #Ouvertutre fichier ech distnace
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    with open('DistnaceRSSI.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=' ')
        for row in spamreader:
            
            if row[1] != "" : 
                print(row)
                sql="SELECT RSSI FROM captureRSSI WHERE numEch = %s" #RECHERCHE LE RSSI CORRESPONDANT A L'ECH
                cursor.execute(sql, (str(row[0]),))
                RSSICapture = cursor.fetchall()
                
                
                if RSSICapture != []:       
                    print(f"Ech {row[0]}  --  {RSSICapture}")
                    row.append(float(RSSICapture[0][0]))  # Assurez-vous que RSSI est un float
                    print(row)
                    writer.writerow(row)                    
                    res.append(row)
                    distance.append(float(row[1]))  # Rajoute dans le tableau resultat valide + Conversion en float
                    rssi.append(float(row[2]))  # Rajoute dans le tableau resultat valide + Conversion en float
print(distance)
print(rssi)

###############################################################
###############################################################
# Transformation logarithmique : RSSI doit être négatif, donc on prend abs()
# Utiliser curve_fit pour ajuster la fonction aux données
params, covariance = curve_fit(model, distance, rssi)

# Extraire les paramètres ajustés a et b
a, b = params
# Afficher les résultats
print(f'Paramètre a: {a}')
print(f'Paramètre b: {b}')
# Créer une plage plus dense de distances pour une courbe plus lisse
distance_fine = np.linspace(min(distance), max(distance), 500)  # 500 points pour plus de précision

courbeEmpirique = model(distance_fine, *params)
# ########################################################




#########################################################
###########TRACER DES DIFFERNTES COURBES#################
#########################################################

# Créer un graphique avec 2 sous-graphiques côte à côte
fig, axs = plt.subplots(1, 2, figsize=(14, 6))  # 1 ligne, 2 colonnes

axs[0].scatter(distance,rssi,  s=10, c='red', label="Wifi distance RSSI")
axs[0].plot(distance_fine,courbeEmpirique , color='blue', label=f"Régression : RSSI = {a:.3f} * log10(dist) + {b:.3f}")
axs[0].grid()
axs[0].set_xlabel('Dist = fct(RSSI)', fontsize=10)
axs[0].set_ylabel("RSSI (dBm)",fontsize=10)
axs[0].set_xlabel("Distance (m)",fontsize=10)
axs[0].legend(fontsize=10)



axs[1].plot(courbeEmpirique ,distance_fine, color='blue', label=f"Dist = .....A ECRIRE")
axs[1].grid()
axs[1].set_title('Dist = fct(RSSI)', fontsize=10)
axs[1].set_xlabel("RSSI (dBm)",fontsize=10)
axs[1].set_ylabel("Distance (m)",fontsize=10)
axs[1].legend(fontsize=10)


# Afficher le graphique
plt.tight_layout()
plt.show()
# ########################################################
