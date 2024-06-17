#include "Adafruit_MPR121.h"
#include <SparkFun_Qwiic_Button.h>
#include <seesaw_neopixel.h>
// #include <Adafruit_TestBed.h>
// extern Adafruit_TestBed TB;

#define SECONDARY_I2C_PORT &Wire1


const int sequenceLength = 10;
const int n = 1;
const int timeout = 3000;
const int foot_button_pin = A1; // analog pin connected to X output
const int throttle_pin = A2; // analog pin connected to X output
const int throttle_th = 2900; // thrashhold for the potentiometer of the throttle

#define  DEFAULT_I2C_ADDR 0x30
#define  ANALOGIN   18
#define  NEOPIXELOUT 14


QwiicButton button;
uint8_t brightness = 100;   //The brightness to set the LED to when the button is pushed
Adafruit_seesaw seesaw;
seesaw_NeoPixel pixels = seesaw_NeoPixel(4, NEOPIXELOUT, NEO_GRB + NEO_KHZ800);

void I2C_setup_for_PyQT(){

  #if defined(ARDUINO_ADAFRUIT_QTPY_ESP32S2) || \
      defined(ARDUINO_ADAFRUIT_QTPY_ESP32S3_NOPSRAM) || \
      defined(ARDUINO_ADAFRUIT_QTPY_ESP32S3) || \
      defined(ARDUINO_ADAFRUIT_QTPY_ESP32_PICO)
    // ESP32 is kinda odd in that secondary ports must be manually
    // assigned their pins with setPins()!
    Wire1.setPins(SDA1, SCL1);
  #endif

  #if defined(ARDUINO_ADAFRUIT_FEATHER_ESP32S2)
    // turn on the I2C power by setting pin to opposite of 'rest state'
    pinMode(PIN_I2C_POWER, INPUT);
    delay(1);
    bool polarity = digitalRead(PIN_I2C_POWER);
    pinMode(PIN_I2C_POWER, OUTPUT);
    digitalWrite(PIN_I2C_POWER, !polarity);
  #endif

  #if defined(ARDUINO_ADAFRUIT_FEATHER_ESP32S2_TFT)
    pinMode(TFT_I2C_POWER, OUTPUT);
    digitalWrite(TFT_I2C_POWER, HIGH);
  #endif

  #if defined(ARDUINO_ADAFRUIT_FEATHER_ESP32S2_REVTFT)
    pinMode(TFT_I2C_POWER, OUTPUT);
    digitalWrite(TFT_I2C_POWER, HIGH);
  #endif

  #if defined(ADAFRUIT_FEATHER_ESP32_V2)
    // Turn on the I2C power by pulling pin HIGH.
    pinMode(NEOPIXEL_I2C_POWER, OUTPUT);
    digitalWrite(NEOPIXEL_I2C_POWER, HIGH);
  #endif

}


bool isPressed(int pin, int thr){

  int deg;
  
  if (thr == throttle_th){
    deg = map(analogRead(pin), 2530, 8191, 850, 3100);
    // Serial.println(deg);
  }
  else {
    deg = analogRead(pin);
  }
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

String YesOrNo_foot_button(int foot_button_pin){
  uint32_t  start_time;
  uint32_t  start_time_pressed;
  uint32_t  diff;

  start_time = millis();
  while (true) {
      if(! digitalRead(foot_button_pin)){  
          start_time_pressed = millis();
          while (! digitalRead(foot_button_pin)){
            // Serial.print(".");
          }
          diff = millis() - start_time_pressed;
          if(diff <= 500){
              Serial.println("no");
              return "no";
          }
          else{
              Serial.println("yes");
              return "yes";
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


String YesOrNo_gearshifter(Adafruit_seesaw seesaw){
  uint32_t  start_time;
  int mapped_val = map(seesaw.analogRead(ANALOGIN), 0, 1023, 1, 3);
  Serial.println(mapped_val);
  delay(700);
  start_time = millis();
  while (true) {
      if(mapped_val == 1){ 
          return "yes"; 
          break;
      }
      if(mapped_val == 3){ 
          return "no";
          break;
      }
      else{
          if(millis() - start_time > timeout){
            return "timeout";
            delay(700);
            break;
          } 
      }
  }            
}


String YesOrNo_throttle(int throttle_pin){
  uint32_t  start_time;
  uint32_t  start_time_pressed;
  uint32_t  diff;

  start_time = millis();
  while (true) {
      if(isPressed(throttle_pin, throttle_th)){  
          start_time_pressed = millis();
          while (isPressed(throttle_pin, throttle_th)){
            // Serial.print(".");
          }
          diff = millis() - start_time_pressed;
          if(diff <= 500){
              Serial.println("no");
              return "no";
          }
          else{
              Serial.println("yes");
              return "yes";
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


// Function to run the N-back task
void nBackTask(const std::vector<int>& sequence, int n, int input_type) {

    int correctCount = 0;
    String userInput;

    for (int i = 0; i < sequence.size(); ++i) {
        sendRequest("nback", String(std::to_string(sequence[i]).c_str()));
        Serial.println("\n\"" + String(std::to_string(sequence[i]).c_str()) + "\"");
        delay(200);
        Serial.print("Match? -> ");
        switch (input_type)
        {
        case 0: // button
          userInput = YesOrNo_button(button);
          break;
        case 1: // gearshifter
          userInput = YesOrNo_gearshifter(seesaw);
          break;
        case 3:
          userInput = YesOrNo_foot_button(foot_button_pin);
          break;
        case 4:
          userInput = YesOrNo_throttle(throttle_pin);
          break;
        
        default:
          break;
        }

        if (assert_result(i, sequence, userInput)) {
            correctCount++;
        }
        delay(1000);
    }

    double accuracy = static_cast<double>(correctCount) / sequenceLength * 100;
    Serial.print("Accuracy: ");
    Serial.print(accuracy);
    sendRequest("nback", String(accuracy, DEC));
    sendRequest("nback",  "end");
}

