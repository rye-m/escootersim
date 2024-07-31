#include <network.h>
#include <utils.h>
#include <setupFunc.h>

#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <WebSocketsClient.h>
#include <WiFiMulti.h>
#include <WiFiClientSecure.h>

#include "Adafruit_MPR121.h"
#include <SparkFun_Qwiic_Button.h>
#include <seesaw_neopixel.h>

#include <spotify_button.hpp>
#include <nback_button.hpp>
#include <spotify_foot_button.hpp>
#include <nback_foot_button.hpp>
#include <spotify_throttle.hpp>
#include <nback_throttle.hpp>
#include <nback_watch.hpp>
#include <Arduino.h>


bool log_valid(String text){
    if (text == "mode: Spotify_button"
     ||  text == "mode: Spotify_foot_button"
     ||  text == "mode: Spotify_throttle"
     ||  text == "mode: Nback_button"
     ||  text == "mode: Nback_foot_button"
     ||  text == "mode: Nback_throttle"
     ||  text == "mode: Nback_watch"
     ||  text == "mode: web"
    ){return false;}
    else {return true;}    
}



bool loop_loop(void (*function)()) {
    global_payload = "";
    while(log_valid(global_payload)){
        webSocket.loop();
        (*function)();
    }
    return true;

}


void setup(){
  init_wifi();
	webSocket.begin(ipaddress, port);
	webSocket.onEvent(webSocketEvent);
	webSocket.setReconnectInterval(120000);
}


void loop() {

    webSocket.loop();
    // Serial.print("-");
    if(global_type == WStype_TEXT){

      if(global_payload == "mode: Spotify_button"){
        spotify_button_setup();
        loop_loop(spotify_button_loop);
      }
      else if(global_payload == "mode: Spotify_foot_button"){
        spotify_foot_button_setup();
        loop_loop(spotify_foot_button_loop);
      }
      else if(global_payload == "mode: Spotify_throttle"){
        spotify_throttle_setup();
        loop_loop(spotify_throttle_loop);
      }
      else if(global_payload == "mode: Nback_button"){
        nback_button_setup();
        loop_loop(nback_button_loop);
      }
      else if(global_payload == "mode: Nback_foot_button"){
        nback_foot_button_setup();
        loop_loop(nback_foot_button_loop);
      }
      else if(global_payload == "mode: Nback_throttle"){
        nback_throttle_setup();
        loop_loop(nback_throttle_loop);
      }
      else if(global_payload == "mode: Nback_watch"){ 
        nback_throttle_setup();
        loop_loop(nback_watch_loop);
      }
    }
    // Serial.println("global_payload: " + global_payload);
}