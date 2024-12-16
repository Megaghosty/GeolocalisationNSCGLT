import csv
import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
from statsmodels.regression.quantile_regression import QuantReg
from scipy.optimize import curve_fit  # Pour ajuster une courbe exponentielle
from scipy.stats import linregress  


conn = mysql.connector.connect(host="192.168.1.________",
                                      user="root",
                                      password="root",
                                      database="______________" ) #Nom de la base


cursor = conn.cursor()

res=[]
distance=[]
rssi =[]

#Creation d'un 3-uple => numEch / RSSI / Distance quand cela est possible

with open('echDistance.csv', newline='') as csvfile:                #Ouverture fichier numEch/distance Créer durant la capture
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    with open('DistanceRSSI.csv', 'w', newline='') as file:         #Création d'un fichier qqui va contenir numEch / RSSI / Distance
        writer = csv.writer(file, delimiter=' ')
        for row in spamreader:
            
            if row[1] != "" : 
                print(row)
                sql="SELECT RSSI FROM captureRSSI WHERE numEch = %s"
                cursor.execute(sql, (str(row[0]),))
                RSSICapture = cursor.fetchall()
                if RSSICapture != []:
                    print(f"Ech {row[0]}  --  {RSSICapture}")
                    row.append(float(RSSICapture[0][0]))  # Assurez-vous que RSSI est un float
                    print(row)
                    writer.writerow(row)
                    res.append(row)
                    distance.append(float(row[1]))  
                    rssi.append(float(row[2])) 
print(distance)
print(rssi)

###############################################################
#########REGRESSION LOG##################################

# Transformation logarithmique : RSSI doit être négatif, donc on prend abs()
log_rssi = np.log(np.abs(rssi))

slope, intercept, r_value, p_value, std_err = linregress(log_rssi, distance)

# Afficher les coefficients
print(f"Équation ajustée : y = {slope:.3f} * log(|x|) + {intercept:.3f}")
print(f"R^2 = {r_value**2:.3f}")

# Prédictions pour tracer la courbe ajustée
log_rssi_fit = np.linspace(min(log_rssi), max(log_rssi), 500)  # Points pour log(RSSI)
distance_fit = slope * log_rssi_fit + intercept  # Calculer les distances correspondantes

# Reconvertir log(|RSSI|) en RSSI pour le graphique
rssi_fit = np.exp(log_rssi_fit)  # Appliquer exp pour revenir à RSSI positif
rssi_fit = -rssi_fit  # Réappliquer le signe négatif pour RSSI

# ########################################################
# ########################################################

#AFFICHAGE DES POINTS ET DE LA REGRESSION
plt.scatter(rssi,distance,  s=10, c='red', label="Wifi etalllonnage distance")
plt.plot(rssi_fit, distance_fit, color='blue', label=f"Régression : y = {slope:.3f} * log(|x|) + {intercept:.3f}")


plt.grid()
plt.title('Dist = fct(RSSI)', fontsize=10)
plt.xlabel("RSSI (dBm)",fontsize=10)
plt.ylabel("Distance (m)",fontsize=10)
plt.legend(fontsize=10)
plt.show()
# ########################################################
        
#Exemple pour UN RSSI
print(f"Slope : {slope}")

print(f"Intercept {intercept}")

resEx = slope*np.log(np.abs(-60)) + intercept
print(resEx)   
            