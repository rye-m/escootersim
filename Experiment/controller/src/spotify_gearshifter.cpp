#include <WiFi.h>
#include <network.h>
#include <others.h>
#include <setupFunc.h>
#include <HTTPClient.h>
#include <Wire.h>
#include "Adafruit_MPR121.h"
#include <SparkFun_Qwiic_Button.h>
#include <seesaw_neopixel.h>

#define  DEFAULT_I2C_ADDR 0x30
#define  ANALOGIN   18
#define  NEOPIXELOUT 14

    int next_e = 60;
    int play_b = 230;
    int play_e = 370;
    int pause_b = 400;
    int pause_e = 710;
    int previous_b = 720;


// // const int X_pin = 32; // analog pin connected to X output
String current_input = "none";
String previous_input = "pause";

// SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
// SPDX-License-Identifier: MIT
/*
 * This example shows how read the potentiometer on the I2C QT Slide Potentiometer
 * and make the NeoPixels change too!
 */

Adafruit_seesaw seesaw;
seesaw_NeoPixel pixels = seesaw_NeoPixel(4, NEOPIXELOUT, NEO_GRB + NEO_KHZ800);
// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return seesaw_NeoPixel::Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return seesaw_NeoPixel::Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return seesaw_NeoPixel::Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}

void setup() {
  init_wifi();

  
  uint16_t pid;
  uint8_t year, mon, day;

  seesaw.getProdDatecode(&pid, &year, &mon, &day);
  Serial.print("seesaw found PID: ");
  Serial.print(pid);
  Serial.print(" datecode: ");
  Serial.print(2000+year); Serial.print("/");
  Serial.print(mon); Serial.print("/");
  Serial.println(day);

  if (pid != 5295) {
      Serial.println(F("Wrong seesaw PID"));
      while (1) delay(10);
  }

  if (!pixels.begin(DEFAULT_I2C_ADDR)){
      Serial.println("seesaw pixels not found!");
      while(1) delay(10);
  }

  Serial.println(F("seesaw started OK!"));

  pixels.setBrightness(255);  // half bright
  pixels.show(); // Initialize all pixels to 'off'

  sendRequest("api",  "first_contact");
}




void loop() {
  // read the potentiometer
  uint16_t slide_val = seesaw.analogRead(ANALOGIN);
//   int mapped_val = map(seesaw.analogRead(ANALOGIN), 0, 1023, 1, 1000);


    Serial.println(slide_val);
    if (slide_val <= next_e){
            Serial.println("next");
            sendRequest("api",  "next");
            previous_input = "next";
    }
    else if (play_b < slide_val && slide_val <= play_e){
            sendRequest("api",  "play");
            Serial.println("play");
            previous_input = "play";
    }
    else if (pause_b < slide_val && slide_val <= pause_e){
            Serial.println("pause");
            sendRequest("api",  "pause");
            previous_input = "pause";
    }
    else if (previous_b <= slide_val){
            Serial.println("previous");
            sendRequest("api",  "previous");
            previous_input = "previous";
    }

    for (uint8_t i=0; i< pixels.numPixels(); i++) {
        pixels.setPixelColor(i, Wheel(slide_val / 4));
        }
        pixels.show();
  
  delay(50);
}





// // Arduino pin numbers
// const int X_pin = 0; // analog pin connected to X output

// void setup() {
//   Serial.begin(115200);
// }

// void loop() {
//   int deg = analogRead(X_pin);
//   Serial.println(deg);
//   // Serial.println(map(deg, 920, 1025, 55, -55));
//   // if (deg < 250) Serial.println(map(deg, 0, 250, -180, 0));
//   // else Serial.println(map(deg, 250, 500, 0, 180));
//   delay(50);
// }



// void loop() {
//   // read the potentiometer
//   uint16_t slide_val = seesaw.analogRead(ANALOGIN);
//   int mapped_val = map(seesaw.analogRead(ANALOGIN), 0, 1023, 1, 6);
//   // Serial.println(slide_val);

//   if (previous_input != mapped_val){
//     switch(mapped_val){
//     case 3:
//             Serial.println("case 2: next");
//             changeColor(2, pixels);
//             sendRequest("api",  "next");
//             break;
//     case 4:
//             Serial.println("case 3: play");
//             changeColor(3, pixels);
//             sendRequest("api",  "play");
//             break;
//     case 5:
//             Serial.println("case 4: pause");
//             changeColor(4, pixels);
//             sendRequest("api",  "pause");
//             break;
//     case 6:
//             Serial.println("case 5: previous");
//             changeColor(5, pixels);
//             sendRequest("api",  "previous");
//             break;
//     default:
//           break;
//     }
//   }            

//   previous_input = mapped_val;
//   delay(50);
// }

