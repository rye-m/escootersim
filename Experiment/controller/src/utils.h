#include "Adafruit_MPR121.h"
#include <SparkFun_Qwiic_Button.h>
#include <seesaw_neopixel.h>

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
uint8_t brightness = 100;   //The brightness to set the LED to when the button is pushed


String flg;
int shifter_no;
int data[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int new_data[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int previous_shift_no = 99;

int one_up_bgn = 910;
int one_up_end = 926;
int two_up_bgn = 815;
int two_up_end = 860;
int three_up_bgn = 763;
int three_up_end = 820;
int four_up_bgn = 713;
int four_up_end = 756;
int five_up_bgn = 658;
int five_up_end = 711;
int six_up_bgn = 598;
int six_up_end = 612;
int one_down_bgn = 924;
int one_down_end = 995;
int two_down_bgn = 840;
int two_down_end = 871;
int three_down_bgn = 782;
int three_down_end = 812;
int four_down_bgn = 730;
int four_down_end = 764;
int five_down_bgn = 676;
int five_down_end = 704;
int six_down_bgn = 601;
int six_down_end = 612;

QwiicButton button;
Adafruit_seesaw seesaw(&Wire1);
seesaw_NeoPixel pixels = seesaw_NeoPixel(4, NEOPIXELOUT, NEO_GRB + NEO_KHZ800);


void gearshifter_setup() {
  Wire1.begin();
  if (!seesaw.begin(DEFAULT_I2C_ADDR)) {
    Serial.println(F("seesaw not found!"));
    while(1) delay(10);
  }
  delay(500);
  Serial.println(F("seesaw found!"));
}

int read_gearshifter() {
  int raw_val = seesaw.analogRead(ANALOGIN);
  Serial.print(raw_val);

  if (data[0] > raw_val){
    if (one_up_bgn < raw_val and raw_val < one_up_end){ shifter_no = 1; flg = "up";}
    else if (two_up_bgn < raw_val and raw_val < two_up_end){ shifter_no = 2; flg = "up";}
    else if (three_up_bgn < raw_val and raw_val < three_up_end){ shifter_no = 3; flg = "up";}
    else if (four_up_bgn < raw_val and raw_val < four_up_end){ shifter_no = 4; flg = "up";}
    else if (five_up_bgn < raw_val and raw_val < five_up_end){ shifter_no = 5; flg = "up";}
    else if (six_up_bgn < raw_val and raw_val < six_up_end){ shifter_no = 6; flg = "up";}
    else {flg = "up";}
  } 
  else if (data[0] < raw_val){
    if (one_down_bgn < raw_val and raw_val < one_down_end){ shifter_no = 1; flg = "down";}
    else if (two_down_bgn < raw_val and raw_val < two_down_end){ shifter_no = 2; flg = "down";}
    else if (three_down_bgn < raw_val and raw_val < three_down_end){ shifter_no = 3; flg = "down";}
    else if (four_down_bgn < raw_val and raw_val < four_down_end){ shifter_no = 4; flg = "down";}
    else if (five_down_bgn < raw_val and raw_val < five_down_end){ shifter_no = 5; flg = "down";}
    else if (six_down_bgn < raw_val and raw_val < six_down_end){ shifter_no = 6; flg = "down";}
    else {flg = "down";}
  }
  else {flg = "stay";}

  Serial.print(",\t");
  Serial.print(data[0]);
  Serial.print(",\t");
  Serial.print(shifter_no);
  Serial.print(",\t");
  Serial.println(flg);

  for (int i = 0; i < 9; i++) {
    new_data[i] = data[i+1];
  }
  new_data[9] = raw_val;
  for (int i = 0; i < 10; i++){
      data[i] = new_data[i];
  }
  return shifter_no;
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
  uint32_t  start_time = millis();
  int yn_previous_shift_no = 2;

  while (true) {
    int yn_shift_no = read_gearshifter();

    if(yn_shift_no == yn_previous_shift_no){
      yn_previous_shift_no = yn_shift_no;
    }
    else if(yn_shift_no != yn_previous_shift_no){    
      if(yn_shift_no == 1){ 
          return "yes"; 
          break;
      }
      if(yn_shift_no == 3){ 
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
    else if (millis() - start_time > timeout){
            return "timeout";
            delay(700);
            break;
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

