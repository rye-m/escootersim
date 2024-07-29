/*
 * WebSocketClient.ino
 *
 *  Created on: 24.05.2015
 *
 */

#include <Arduino.h>

#include <WiFi.h>
#include <Wire.h>
#include <WiFiMulti.h>
#include <WiFiClientSecure.h>

#include <WebSocketsClient.h>


WiFiMulti WiFiMulti;


void nback_watch_setup() {
	Serial.setDebugOutput(true);
}

void nback_watch_loop() {

  while (true){
    webSocket.loop();
    if (global_payload == "start_nback"){
      sendRequest("nback",  "begin");
      delay(2000);
      nBackTask(5);
      break;
    }
  }
}