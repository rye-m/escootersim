#include <network.h>
#include <utils.h>
#include <setupFunc.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include "Adafruit_MPR121.h"
#include <SparkFun_Qwiic_Button.h>
#include <seesaw_neopixel.h>
#include <spotify_button.hpp>
#include <nback_button.hpp>
#include <spotify_foot_button.hpp>
#include <nback_foot_button.hpp>
#include <spotify_footpedal.hpp>
#include <nback_footpedal.hpp>
#include <spotify_gearshifter.hpp>
#include <nback_gearshifter.hpp>
#include <spotify_throttle.hpp>
#include <nback_throttle.hpp>
#include <nback_watch.hpp>
#include <Arduino.h>


int res_code = 0;

void setup(){
    init_wifi();

    res_code = sendRequest("mode_tinypico");
    Serial.println(res_code);
    switch(res_code) {
        case 201:
            Serial.println("spotify_button_setup");
            spotify_button_setup();
            break;
        case 202:
            Serial.println("spotify_footpedal_setup");
            spotify_footpedal_setup();
            break;
        case 203:
            Serial.println("spotify_gearshifter_setup");
            spotify_gearshifter_setup();
            break;
        case 204:
            Serial.println("spotify_throttle_setup");
            spotify_throttle_setup();
            break;
        case 205:
            Serial.println("nback_button_setup");
            nback_button_setup();
            break;
        case 206:
            Serial.println("nback_footpedal_setup");
            nback_footpedal_setup();
            break;
        case 207:
            Serial.println("nback_gearshifter_setup");
            nback_gearshifter_setup();
            break;
        case 208:
            Serial.println("nback_throttle_setup");
            nback_throttle_setup();
            break;
        case 209:
            Serial.println("spotify_foot_button_setup");
            spotify_foot_button_setup();
            break;
        case 210:
            Serial.println("nback_foot_button_setup");
            nback_foot_button_setup();
            break;
        case 211:
            Serial.println("nback_watch_setup");
            // nback_watch_setup();
            break;
        default:
            Serial.println("default");
            break;
        }
}


void loop() {
    switch(res_code) {
        case 201:
            spotify_button_loop();
            break;
        case 202:
            spotify_footpedal_loop();
            break;
        case 203:
            spotify_gearshifter_loop();
            break;
        case 204:
            spotify_throttle_loop();
            break;
        case 205:
            nback_button_loop();
            break;
        case 206:
            Serial.println("206");
            nback_gearshifter_loop();
            break;
        case 207:
            nback_gearshifter_loop();
            break;
        case 208:
            nback_throttle_loop();
            break;
        case 209:
            spotify_foot_button_loop();
            break;
        case 210:
            nback_foot_button_loop();
            break;
        case 211:
            // nback_watch_loop();
            break;
        default:
            Serial.print("default: ");
            Serial.println(res_code);
            break;
        }
    }