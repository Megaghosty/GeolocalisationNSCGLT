#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// Paramètres des trois bornes WiFi
const char* ssids[] = {"CIEL1", "CIEL2", "CIEL3"};
const char* passwords[] = {"WCIELB2111", "WCIELB2112", "WCIELB2113"};
const int NUM_NETWORKS = 3;
const int SAMPLES_PER_NETWORK = 20;  // Modifié à 20 échantillons par borne

// Paramètres du serveur MQTT
const char* mqtt_server = "192.168.1.20";
const int mqtt_port = 1883;
const char* mqtt_topic = "numeEch/RSSI";

int ech_index = 1;
int current_network = 0;
int samples_count = 0;

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi(int network_index) {
  WiFi.disconnect();
  delay(100);
  
  Serial.println("Connexion au WiFi...");
  WiFi.begin(ssids[network_index], passwords[network_index]);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\nConnecté au réseau WiFi!");
  Serial.print("SSID: ");
  Serial.println(ssids[network_index]);
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
  setup_wifi(current_network);
  client.setServer(mqtt_server, mqtt_port);
  Serial.println("Appuyez sur Entrée pour commencer les mesures...");
}

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

void switchToNextNetwork() {
  current_network++;
  if (current_network < NUM_NETWORKS) {
    setup_wifi(current_network);
    samples_count = 0;
    Serial.println("Passage à la borne suivante. Appuyez sur Entrée pour continuer...");
  } else {
    Serial.println("Toutes les mesures sont terminées.");
    while(1); // Arrêt du programme
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  if (checkSerialInput() || samples_count > 0) {
    int rssi = WiFi.RSSI();

    Serial.print("Borne ");
    Serial.print(current_network + 1);
    Serial.print(" - Ech ");
    Serial.print(ech_index);
    Serial.print(" --- RSSI : ");
    Serial.print(rssi);
    Serial.println(" dBm");

    StaticJsonDocument<200> jsonDoc;
    jsonDoc["borne"] = current_network + 1;
    jsonDoc["num_echantillon"] = ech_index;
    jsonDoc["valeur_Rssi"] = rssi;

    char jsonBuffer[200];
    serializeJson(jsonDoc, jsonBuffer);

    client.publish(mqtt_topic, jsonBuffer);

    ech_index++;
    samples_count++;

    if (samples_count >= SAMPLES_PER_NETWORK) {
      switchToNextNetwork();
    } else {
      Serial.println("Appuyez sur Entrée pour l'échantillon suivant...");
    }

    delay(1000); // Attente d'une seconde entre chaque échantillon
  }
}
