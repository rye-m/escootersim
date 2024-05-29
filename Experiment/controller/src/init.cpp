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
#include <nback_gearshifter.hpp>
#include <spotify_footpedal.hpp>
#include <spotify_gearshifter.hpp>
#include <Arduino.h>


int res_code = 0;

void setup(){
    init_wifi();

    res_code = sendRequest("mode_tinypico");
    Serial.println(res_code);
    switch(res_code) {
        case 201:
            Serial.println("201");
            spotify_button_setup();
            break;
        case 202:
            Serial.println("202");
            spotify_footpedal_setup();
            break;
        case 203:
            Serial.println("203");
            spotify_gearshifter_setup();
            break;
        case 204:
            Serial.println("204");
            break;
        case 205:
            Serial.println("205");
            nback_button_setup();
            break;
        case 206:
            Serial.println("206");
            // nback_footpedal_setup();
            break;
        case 207:
            Serial.println("207");
            nback_gearshifter_setup();
            break;
        case 208:
            Serial.println("208");
            break;
        case 209:
            Serial.println("208");
            spotify_foot_button_setup();
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
            Serial.println("204");
            break;
        case 205:
            Serial.println("205");
            nback_button_loop();
            break;
        case 206:
            Serial.println("206");
            // nback_gearshifter_loop();
            break;
        case 207:
            Serial.println("207");
            nback_gearshifter_loop();
            break;
        case 208:
            Serial.println("208");
            break;
        case 209:
            Serial.println("209");
            spotify_foot_button_loop();
            break;
        default:
            Serial.println("default");
            break;
        }
    }