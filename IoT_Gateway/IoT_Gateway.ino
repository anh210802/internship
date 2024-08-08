#include <WiFi.h>
#include <WiFiMulti.h>
#include <Wire.h>

const char* ssid = ""; //ssid of your wifi
const char* password = ""; // password of your wifi
const int portname = 2108;
String node_data_string;
int flag_send_data = 0;
String data_public;
WiFiClient client;  

void connectWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());
}

void connectTCP() {
  while (!client.connected()) {
    Serial.println("Connecting to host...");
    if (client.connect(IPAddress(177,30,34,202), portname)) {
      Serial.println("Connected to host");
    } else {
      Serial.println("Connection to host failed, retrying...");
      delay(1000);
    }
  }
}

void sendDataToServer() {
  if (flag_send_data == 1) {
    client.print(data_public);
    flag_send_data = 0;
  }
}

void readDataNode() {
  while (Serial2.available()) {
    node_data_string = Serial2.readStringUntil('\n');
    node_data_string.trim();
    Serial.print("STR: ");
    Serial.println(node_data_string);
    
    if (node_data_string.startsWith("1")) {
      data_public = node_data_string;
      flag_send_data = 1;
    }
  }
}

void setup() {
  Serial.begin(115200);
  Serial2.begin(115200);

  connectWiFi();
  connectTCP();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }
  
  if (!client.connected()) {
    connectTCP();
  }

  readDataNode();
  sendDataToServer();
}
