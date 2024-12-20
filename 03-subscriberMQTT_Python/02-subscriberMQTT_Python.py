import paho.mqtt.client as mqtt
import json
import mysql.connector

# Paramètres MQTT
MQTT_SERVER = "192.168.1.20"  # Adresse IP ou nom de domaine du serveur MQTT
MQTT_PORT = 1883  # Port du serveur MQTT
MQTT_TOPIC = "numeEch/RSSI"  # Topic MQTT

####
conn = mysql.connector.connect(host="192.168.1.20",
                                      user="root",
                                      password="root",
                                      database="mesure_esp32" ) #Nom de la base

cursor = conn.cursor()


cursor.execute("SELECT * FROM mesureESP32")   #NOM DE LA TABLE

myresult = cursor.fetchall()

for x in myresult:
  print(x)

# Callback lorsque la connexion au serveur est établie
def on_connect(client, userdata, flags, rc):
    print(f"Connecté au serveur MQTT avec le code de retour {rc}")
    client.subscribe(MQTT_TOPIC)

# Callback lorsque un message est reçu
def on_message(client, userdata, msg):
    try:
        # Décoder le message JSON
        payload = msg.payload.decode()
        data = json.loads(payload)
        print(f"Échantillon: {data['num_echantillon']}, Valeur en dbm: {data['valeur_Rssi']}")
        
        # Préparer et exécuter la requête SQL
        sql = "INSERT INTO mesureESP32 (num_echantillon, valeur_Rssi,date_capture) VALUES (%s, %s, CURRENT_TIMESTAMP)"
        values = (data['num_echantillon'], data['valeur_Rssi'])
        cursor.execute(sql, values)
        conn.commit()
        
        print("++++++++++++++++++++++++++++++++++++Dans BDD")
    except json.JSONDecodeError:
        print(f"Erreur: Message reçu non JSON valide {payload}")
    except mysql.connector.Error as err:
        print(f"Erreur MySQL: {err}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, MQTT_PORT, 60)

# Boucle pour attendre les messages
try:
    print("En attente des messages MQTT...")
    client.loop_forever()
except KeyboardInterrupt:
    print("Arrêt du client MQTT.")
    client.disconnect()
finally:
    cursor.close()
    conn.close()
    print("Connexion à la base de données fermée.")
