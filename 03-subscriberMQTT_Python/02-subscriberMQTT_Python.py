import paho.mqtt.client as mqtt
import json
import mysql.connector

# Paramètres MQTT
MQTT_SERVER = "192.168.1.__________"  # Adresse IP ou nom de domaine du serveur MQTT
MQTT_PORT = 1883  # Port du serveur MQTT
MQTT_TOPIC = "_______/________"  # Topic MQTT

####
conn = mysql.connector.connect(host="192.168.1.________",
                                      user="root",
                                      password="root",
                                      database="______________" ) #Nom de la base

cursor = conn.cursor()


cursor.execute("SELECT * FROM __________")   #NOM DE LA TABLE

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
        print(f"Échantillon: {data['sample_index']}, Température: {data['rssi']}")
        
        #A VOUS DE METTRE DANS LA TABLE data['sample_index'] et str(data['rssi'])
        
        sql = "INSERT _______"
        _______________________
        _______________________
        _______________________
        print("++++++++++++++++++++++++++++++++++++Dans BDD")
    except json.JSONDecodeError:
        print(f"Erreur: Message reçu non JSON valide {payload}")

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
