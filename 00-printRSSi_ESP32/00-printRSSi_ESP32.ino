#include <WiFi.h>

const char* ssid = "_______";
const char* password = "____________";

void setup() {
  Serial.begin(115200);

  // Connexion au réseau Wi-Fi
  Serial.println("Connexion au Wi-Fi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  
  Serial.println("\nConnecté au Wi-Fi.");
  Serial.print("Adresse IP : ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Récupération du RSSI
  int rssi = WiFi.RSSI();
  Serial.print("RSSI : ");
  Serial.print(rssi);
  Serial.println(" dBm");

  delay(2000); // Attendre 5 secondes avant de mettre à jour
}
