// #include <Arduino.h>
#include <WiFi.h>
#include <network.h>
#include <Wire.h>
#include "Adafruit_MPR121.h"
#include <SparkFun_Qwiic_Button.h>
#include "Adafruit_seesaw.h"
#include <seesaw_neopixel.h>

#define  DEFAULT_I2C_ADDR 0x30
#define  ANALOGIN   18
#define  NEOPIXELOUT 14

Adafruit_seesaw seesaw;
seesaw_NeoPixel pixels = seesaw_NeoPixel(4, NEOPIXELOUT, NEO_GRB + NEO_KHZ800);

// const int X_pin = 32; // analog pin connected to X output
int previous_input = 0;

int sendRequest(String);
void changeColor(int);


void setup(){
    Serial.begin(115200);
    delay(1000);

    WiFi.mode(WIFI_STA); //Optional
    WiFi.begin(ssid, password);
    Serial.println("\nConnecting");

    while(WiFi.status() != WL_CONNECTED){
        Serial.print(".");
        delay(100);
    }

    Serial.println("\nConnected to the WiFi network");
    Serial.print("Local TinyPICO IP: ");
    Serial.println(WiFi.localIP());

    delay(1000);

    Serial.println(F("Adafruit PID 5295 I2C QT Slide Potentiometer test!"));
    if (!seesaw.begin(DEFAULT_I2C_ADDR)) {
        Serial.println(F("seesaw not found!"));
        while(1) delay(10);
    }
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

    sendRequest("first_contact");
}


void loop() {
  // read the potentiometer
  uint16_t slide_val = seesaw.analogRead(ANALOGIN);
  int mapped_val = map(seesaw.analogRead(ANALOGIN), 0, 1023, 1, 6);
  // Serial.println(slide_val);

  if (previous_input != mapped_val){
    switch(mapped_val){
    case 3:
            Serial.println("case 2: next");
            changeColor(2);
            sendRequest("next");
            break;
    case 4:
            Serial.println("case 3: play");
            changeColor(3);
            sendRequest("play");
            break;
    case 5:
            Serial.println("case 4: pause");
            changeColor(4);
            sendRequest("pause");
            break;
    case 6:
            Serial.println("case 5: previous");
            changeColor(5);
            sendRequest("previous");
            break;
    default:
          break;
    }
  }            

  previous_input = mapped_val;
  delay(50);
}



// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
void changeColor(int status) {
    int color;

    switch (status){
        case 2:
          color = 0xEC3440;
        case 3:
          color = 0xFDD503;
        case 4:
          color = 0x02AFD7;
        case 5:
          color = 0x6C2EB9;

    for (uint8_t i=0; i< pixels.numPixels(); i++) {
        pixels.setPixelColor(0, color);
        pixels.show();
    }
  }
}