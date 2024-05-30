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

const int A1 = 32; // analog pin connected to X output

void setup() {
  Serial.begin(112000);
  pinMode(A1, INPUT);  // set our pin to an input with a pullup resistor
}

void loop() {
    Serial.println(analogRead(A1));// do something like blink pin 13 LED, or whatever
    delay(200);
  // read the state of the pushbutton value - if not activated low then loop
//   if( ! digitalRead(A1) ) {
//     Serial.println(digitalRead(A1));// do something like blink pin 13 LED, or whatever
//   }
//   else {
//     Serial.println(".");// do something like blink pin 13 LED, or whatever
//   }
}