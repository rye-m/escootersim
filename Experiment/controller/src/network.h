#pragma once
#include <HTTPClient.h>


// const char *ssid = "deviceFarm";
// const char *password = "device@theFarm";
// const String ipaddress = "192.168.1.103"; // Type "ipconfig getifaddr en0" in Terminal 
const uint16_t port = 8888; // Default port

const char *ssid = "Enoki";
const char *password = "W0nton$oup";
const String ipaddress = "192.168.1.2"; // Type "ipconfig getifaddr en0" in Terminal 

// const char *ssid = "AIRLab";
// const char *password = "AIRLab2023";
// const String ipaddress = "192.168.0.103";

// const char *ssid = "TP-Link_D18C";
// const char *password = "51283841";
// const String ipaddress = "192.168.0.109";


int sendRequest(String path) {
  // Conect to the WiFi
  HTTPClient http;

  String serverPath = "http://" + ipaddress + ":" + port + "/" + path;
  Serial.print("URL: ");  Serial.print(serverPath);
  // Your Domain name with URL path or IP address with path
  http.begin(serverPath.c_str());
  
  // If you need Node-RED/server authentication, insert user and password below
  //http.setAuthorization("REPLACE_WITH_SERVER_USERNAME", "REPLACE_WITH_SERVER_PASSWORD");
  
  // Send HTTP GET request
  int httpResponseCode = http.GET();
  
  if (httpResponseCode == 200) {
    Serial.print("HTTP Response code: "); Serial.println(httpResponseCode);
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  // Free resources
  http.end();

  return httpResponseCode;
}



int sendRequest(String path, String command) {
  // Conect to the WiFi
  HTTPClient http;

  String serverPath = "http://" + ipaddress + ":" + port + "/" + path + "/" + command;
  Serial.print("URL: ");  Serial.print(serverPath);
  Serial.print(",\tcommand: ");  Serial.println(command);
  // Your Domain name with URL path or IP address with path
  http.begin(serverPath.c_str());
  
  // If you need Node-RED/server authentication, insert user and password below
  //http.setAuthorization("REPLACE_WITH_SERVER_USERNAME", "REPLACE_WITH_SERVER_PASSWORD");
  
  // Specify content-type header
  // http.addHeader("Content-Type", "application/json");

  // Data to send with HTTP POST
  // String httpRequestData = "{\"command\":\"" + command + "\"}";

  // Send HTTP POST request
  int httpResponseCode = http.GET();
  
  if (httpResponseCode == 200) {
    Serial.print("HTTP Response code: "); Serial.println(httpResponseCode);
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  // Free resources
  http.end();

  return httpResponseCode;
}
