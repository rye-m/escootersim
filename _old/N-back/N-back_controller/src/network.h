#include <HTTPClient.h>


const char *ssid = "deviceFarm";
const char *password = "device@theFarm";
const String ipaddress = "192.168.1.103";

int sendRequest(String command) {
  // Conect to the WiFi
  HTTPClient http;

  String serverPath = "http://" + ipaddress + ":8888/nback";
  Serial.print("URL: ");  Serial.print(serverPath);
  Serial.print(",\tcommand: ");  Serial.println(command);
  // Your Domain name with URL path or IP address with path
  http.begin(serverPath.c_str());
  
  // If you need Node-RED/server authentication, insert user and password below
  //http.setAuthorization("REPLACE_WITH_SERVER_USERNAME", "REPLACE_WITH_SERVER_PASSWORD");
  
  // Specify content-type header
  http.addHeader("Content-Type", "application/json");

  // Data to send with HTTP POST
  String httpRequestData = "{\"command\":\"" + command + "\"}";

  // Send HTTP POST request
  int httpResponseCode = http.POST(httpRequestData);
  
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
