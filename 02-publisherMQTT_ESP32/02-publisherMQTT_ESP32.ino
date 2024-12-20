#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h> // Bibliothèque pour JSON

// Paramètres réseau WiFi
const char* ssid = "CIEL1"; 
const char* password = "WCIELB2111"; 

// Paramètres du serveur MQTT
const char* mqtt_server = "192.168.1.20"; // Adresse IP du serveur MQTT
const int mqtt_port = 1883; 
const char* mqtt_topic = "numeEch/RSSI"; // Topic de votre choix
int ech_index;
WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  Serial.println("Connexion au WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnecté au réseau WiFi!");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Connexion au serveur MQTT...");
    if (client.connect("ESP32Client")) {
      Serial.println("connecté!");
    } else {
      Serial.print("Ca craint, rc=");
      Serial.print(client.state());
      Serial.println(" nouvelle tentative dans 5 secondes...");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  ech_index = 1;
  Serial.println("Appuyez sur Entrée pour envoyer la valeur RSSI...");
}

// Nouvelle fonction pour lire l'entrée série
bool checkSerialInput() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      while (Serial.available()) Serial.read(); // Vider le buffer
      return true;
    }
  }
  return false;
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  if (checkSerialInput()) {
    int rssi = WiFi.RSSI();

    // Affichage Info envoyee
    Serial.print("Ech ");
    Serial.print(ech_index);
    Serial.print(" --- RSSI : ");
    Serial.print(rssi);
    Serial.println(" dBm");

    // Création d'un objet JSON
    StaticJsonDocument<200> jsonDoc;
    jsonDoc["num_echantillon"] = ech_index;
    jsonDoc["valeur_Rssi"] = rssi;

    // Conversion en chaîne JSON
    char jsonBuffer[200];
    serializeJson(jsonDoc, jsonBuffer);

    // Publication sur le topic MQTT
    client.publish(mqtt_topic, jsonBuffer);

    ech_index++;  //Incrmeentation numéro échantillion
    Serial.println("Appuyez sur Entrée pour envoyer la prochaine valeur RSSI...");
  }
}
