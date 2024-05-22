#include "Adafruit_MPR121.h"
#include <SparkFun_Qwiic_Button.h>
#include <seesaw_neopixel.h>

const int sequenceLength = 10;
const int n = 1;
const int timeout = 3000;
#define  DEFAULT_I2C_ADDR 0x30
#define  ANALOGIN   18
#define  NEOPIXELOUT 14


QwiicButton button;
uint8_t brightness = 100;   //The brightness to set the LED to when the button is pushed
Adafruit_seesaw seesaw;
seesaw_NeoPixel pixels = seesaw_NeoPixel(4, NEOPIXELOUT, NEO_GRB + NEO_KHZ800);


bool isPressed(int pin, int thr){
  int deg = analogRead(pin);
  if (deg > thr) {
    return true;
  }
  else {
    return false;
  }
}


bool playOrPause() {

    int res = sendRequest("api",  "currently-playing");
    
    if (res == 201) {
        Serial.print("play");
        sendRequest("api",  "play");
    }
    else if (res == 202) {
        Serial.print("pause");
        sendRequest("api",  "pause");
    }

  return true;
}


std::vector<int> generateRandomSequence(int length) {
    std::vector<int> sequence;
    std::uniform_int_distribution<> dis(1, 9); // Generate integers between 1 and 9
    
    Serial.print("sequence: ");
    for (int i = 0; i < length; ++i) {
        int temp = rand() % 10;
        sequence.push_back(temp);
        Serial.print(temp);
    }
      Serial.println("");
    return sequence;
}


String YesOrNo_button(QwiicButton button){
  uint32_t  start_time;
  uint32_t  start_time_pressed;
  uint32_t  diff;

  start_time = millis();
  while (true) {
      if(button.isPressed()){  
          start_time_pressed = millis();
          button.LEDon(100);
          while (button.isPressed()){
            // Serial.print(".");
          }
          button.LEDoff();
          diff = millis() - start_time_pressed;
          if(diff <= 500){
              Serial.println("yes");
              return "yes";
          }
          else{
              Serial.println("no");
              return "no";
          }
          break;
      }
      else{
          if(millis() - start_time > timeout){
            return "timeout";
            break;
          } 
      }
  }            
}


void react(String answer){
    sendRequest("nback", answer);
    Serial.println(answer);
    delay(300);
}

bool assert_result(int i, std::vector<int> sequence, String userInput){

    if (i - n < 0){
        if (userInput == "yes"){
            react("incorrect");
        }
        else if (userInput == "no"){
            react("correct");
            return true;
        }
        else if (userInput == "timeout") {
            react("timedout");
            }
        else {
            Serial.println("Invalid input! Please enter 'y' or 'n'.");
        }
    }
    else{
        if (userInput == "yes") {
            if (sequence[i] == sequence[i - n]) {
                react("correct");
                return true;
            }
            else {
                react("incorrect");
            }
        }
        else if (userInput == "no") {
            if (sequence[i] != sequence[i - n]) {
                react("correct");
                return true;
            }
            else {
                react("incorrect");
            }
        }
        else if (userInput == "timeout") {
            react("timedout");;
            }
        else {
            Serial.println("Invalid input! Please enter 'y' or 'n'.");
        }
    }
    return false;
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
void changeColor(int status, seesaw_NeoPixel pixels) {
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