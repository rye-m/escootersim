#include <Arduino.h>

#include <WiFi.h>
#include <Wire.h>
#include <WiFiMulti.h>
#include <WiFiClientSecure.h>

#include <WebSocketsClient.h>


WiFiMulti WiFiMulti;


void nback_watch_setup() {
	Serial.setDebugOutput(true);
  sendRequest("printout",  "nback_watch_connected");
}

void nback_watch_loop() {
  if (global_payload == "N-back: start_nback"){
    sendRequest("nback",  "begin");
    delay(2000);
    global_payload = "";
    nBackTask(5);
  }
}