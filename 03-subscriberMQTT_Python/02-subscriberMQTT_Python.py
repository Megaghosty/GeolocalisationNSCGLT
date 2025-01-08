import paho.mqtt.client as mqtt
import json
import mysql.connector


# Paramètres MQTT
MQTT_SERVER = "192.168.1.20"
MQTT_PORT = 1883
MQTT_TOPIC = "numeEch/RSSI"

# Fonction pour réinitialiser la table
def reset_table(cursor):
    try:
        cursor.execute("TRUNCATE TABLE mesureESP32")
        print("Table mesureESP32 réinitialisée avec succès.")
    except mysql.connector.Error as err:
        print(f"Erreur lors de la réinitialisation de la table: {err}")

# Connexion à la base de données
conn = mysql.connector.connect(host="192.168.1.20",
                               user="root",
                               password="root",
                               database="mesure_esp32")
cursor = conn.cursor()

# Réinitialisation de la table au démarrage
reset_table(cursor)

# Le reste du code reste inchangé
def on_connect(client, userdata, flags, rc):
    print(f"Connecté au serveur MQTT avec le code de retour {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        print(f"Échantillon: {data['num_echantillon']}, Valeur en dbm: {data['valeur_Rssi']}")
        
        sql = "INSERT INTO mesureESP32 (num_echantillon, valeur_Rssi, date_capture) VALUES (%s, %s, CURRENT_TIMESTAMP)"
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
