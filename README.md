# Projet ESP32 MQTT RSSI : GEoLOCALISATION

Ce dépôt contient plusieurs exemples de code et configurations pour travailler avec un ESP32, MQTT et le traitement des données RSSI.

## Contenu

### 00-printRSSi_ESP32
Un exemple de code permettant de visualiser le RSSI (Received Signal Strength Indicator) directement sur le port série de l'ESP32.

#### Usage
1. Chargez le code sur votre ESP32 via l'IDE Arduino ou toute autre plateforme de développement compatible.
2. Connectez l'ESP32 à un réseau Wi-Fi.
3. Ouvrez le moniteur série pour afficher le RSSI en temps réel.

### 01-mosquitto
Un fichier `docker-compose.yml` pour déployer un conteneur Mosquitto (broker MQTT).

#### Usage.
1. Placez-vous dans le répertoire `01-mosquitto`.
2. Lancez la commande :
   ```bash
   docker-compose up -d
   ```
3. Mosquitto sera disponible sur le port 1883.

### 02-publisherMQTT_ESP32
Un exemple de code pour l'ESP32 servant de publisher MQTT, envoyant un couple `numeEch/RSSI` (numéro d'échantillon et RSSI).

#### Usage
1. Configurez les informations réseau (SSID, mot de passe) et les paramètres MQTT (adresse du broker, topic).
2. Chargez le code sur votre ESP32.
3. Vérifiez que les messages contenant le couple `numeEch/RSSI` sont publiés sur le broker MQTT en utilisant la commande :
   ```bash
   mosquitto_sub -h <adresse_broker> -t <topic>
   ```

### 03-subscriberMQTT_Python
Un exemple de subscriber en Python permettant de récupérer les données publiées sur MQTT et les sauvgegarder dans une Bdd.
#### Prérequis
1. Configurer une bdd avec les bonnes tables et attributs

#### Usage
1. Configurez l'adresse du broker et le topic dans le script Python.
2. Lancez le script :
   ```bash
   python subscriber.py
   ```
3. Les couples `numeEch/RSSI` s'afficheront dans la console et devra être 

### 04-traitementPython
Un exemple de traitement en Python. **Ce fichier est un modèle à adapter selon vos protocoles d'étalonnage.**

#### Usage
1. Modifiez le script avec les bonnes confiugrations et les bonnes mesures.
2. Lancez le script :
   ```bash
   python traitement.py
   ```
3. Observez les résultats de votre traitement dans la console ou exportez-les selon vos besoins.

### 05-visualisationLocalisation
Un exemple de visualisation des bornes et des distances en python. **Ce fichier est un modèle à adapter selon vos protocoles d'étalonnage.**
#### Usage
1. Modifiez le script pour récupérer des valeurs réelles de distances dans une bdd
2. Lancez le script :
   ```bash
   python 05-visualisationLocalisation.py
   ```
3. Observer le résultats graphiques
4. 
## Notes
- Ce dépôt est un point de départ et doit être adapté selon vos besoins spécifiques.

