#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h> // Bibliothèque pour JSON


// Paramètres réseau WiFi
const char* ssid = "___________"; 
const char* password = "__________"; 

// Paramètres du serveur MQTT
const char* mqtt_server = "192.168.1.______________"; // Adresse IP du serveur MQTT
const int mqtt_port = 1883; 
const char* mqtt_topic = "______/_______"; // Topic de votre choix
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
}

void loop() {
  int rssi = WiFi.RSSI();

  // Affichage Info envoyee
  Serial.print("Ech ");
  Serial.print(ech_index);

  Serial.print(" --- RSSI : ");
  Serial.print(rssi);
  Serial.println(" dBm");

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

// Création d'un objet JSON
  StaticJsonDocument<200> jsonDoc;
  jsonDoc["sample_index"] = ech_index;
  jsonDoc["rssi"] = rssi;

  // Conversion en chaîne JSON
  char jsonBuffer[200];
  serializeJson(jsonDoc, jsonBuffer);

  // Publication sur le topic MQTT
  client.publish(mqtt_topic, jsonBuffer);


  ech_index++;  //Incrmeentation numéro échantillion
  delay(5000);  // Pause 5 s
