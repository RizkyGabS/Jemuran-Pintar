#include <ESP32Servo.h>
#include <WiFi.h>
#include <WiFiClient.h>
#include <PubSubClient.h>
#include "DHTesp.h"
#include <ArduinoJson.h>

// MQTT Broker dengan mosquitto lokal dan ngrok dengan port baru 
#define MAX_CHARACTER 50
#define MQTT_SERVER "0.tcp.ap.ngrok.io"

char mqtt_topic[] = "Jemuran";
int mqtt_port = 13801;

const char * ssid = "Wokwi-GUEST";
const char * password = "";

WiFiClient espClient;
PubSubClient client(espClient);

// deklarasi pin
int PIN_DHT = 14;
int ldr = 34;
int servoPin = 25;

// inisialisasi object lib
DHTesp dht;
Servo jemuran;

int position = 0;

// Batas servo Menyala
int batast = 27; // Batas suhu
int batasmoist = 30; // Batas Moisture
int batasldr = 31; // Batas Cahaya

int temp = 0;
int hum = 0;

// menghubungkan ke wifi
void setupWifi(){
  Serial.print("Menghubungkan ke ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED){
    delay(5000);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.print("Terhubung ke ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.println("");
}

void setupMqtt(){
  while (!client.connected()){
    Serial.println("Menghubungkan ke MQTT...");

    String idClient = "client-";
    idClient += String(random(0xffff), HEX);

    if (client.connect(idClient.c_str())){
      Serial.println("MQTT terhubung");
      Serial.println();

      client.publish(mqtt_topic, "Perangkat terhubung...");
      client.publish(mqtt_topic, " ");
    }
    else{
      Serial.print("Error: ");
      Serial.print(client.state());
      Serial.println("Mencoba lagi...");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(9600);

  setupWifi();
  client.setServer(MQTT_SERVER, mqtt_port);

  if (!client.connected()){
    setupMqtt();
  }

  // inisiasi DHT
  dht.setup(PIN_DHT, DHTesp::DHT22);

Serial.begin(9600);

jemuran.attach(servoPin);
}

void loop() {
ldr = map(analogRead(34), 0, 4096, 100, 0); // range ldr diubah dari 0-4096 menjadi 0-100
TempAndHumidity data = dht.getTempAndHumidity();
temp = data.temperature;
hum = data.humidity;

// display data ke serial monitor
Serial.println("===================");
Serial.print("Suhu: ");
Serial.println(temp);
Serial.print("Kelembapan: ");
Serial.println(hum);
Serial.print("Cahaya Matahari: ");
Serial.println(ldr);

//jemuran
position = jemuran.read();
Serial.print("Position Servo: ");
Serial.println(position);
if (temp > batast && hum < batasmoist && ldr > batasldr) {
jemuran.write(1);
delay(1000);
Serial.println("Servo Menyala");
}
else {
jemuran.write(180);
delay(1000);
Serial.println("Servo Mati");
}

// json
DynamicJsonDocument doc(1024);
doc["temp"] = temp;
doc["hum"] = hum;
doc["ldr"] = ldr;
doc["position"] = position;

char buffer[256];
serializeJson(doc, buffer);
client.publish(mqtt_topic, buffer);
delay(2000);
}
