#include "Adafruit_MPR121.h"
#include <SparkFun_Qwiic_Button.h>
#include <seesaw_neopixel.h>
#include <WiFiClientSecure.h>
#include <WebSocketsClient.h>

#define SECONDARY_I2C_PORT &Wire1
#define  DEFAULT_I2C_ADDR 0x30
#define  ANALOGIN   18
#define  NEOPIXELOUT 14

QwiicButton button;
Adafruit_seesaw seesaw(&Wire1);
seesaw_NeoPixel pixels = seesaw_NeoPixel(4, NEOPIXELOUT, NEO_GRB + NEO_KHZ800);
WebSocketsClient webSocket;

const int sequenceLength = 10;
const int n = 1;
const int timeout = 4000;
const int foot_button_pin = A2; // analog pin connected to X output
const int throttle_pin = A1; // analog pin connected to X output
const int throttle_th = 2900; // thrashhold for the potentiometer of the throttle

uint8_t brightness = 100;   //The brightness to set the LED to when the button is pushed
WStype_t global_type;
// uint8_t global_payload = 0;
uint8_t yes[3] = {0x59, 0x65, 0x73};
uint8_t no[2] = {0x4e, 0x65};
String global_payload = "";
bool nback_finish_flg = false;


String flg;
int shifter_no;
int data[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int new_data[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int previous_shift_no = 99;

int one_up_bgn = 24;
int one_up_end =33;
int two_up_bgn = 120;
int two_up_end = 130;
int three_up_bgn = 178;
int three_up_end = 185;
int four_up_bgn = 232;
int four_up_end = 282;
int five_up_bgn = 290;
int five_up_end = 296;
int six_up_bgn = 374;
int six_up_end = 380;
int one_down_bgn = 0;
int one_down_end = 3;
int two_down_bgn = 4;
int two_down_end = 101;
int three_down_bgn = 105;
int three_down_end = 153;
int four_down_bgn = 160;
int four_down_end = 208;
int five_down_bgn = 212;
int five_down_end = 268;
int six_down_bgn = 272;
int six_down_end = 375;


void gearshifter_setup() {
  Wire1.begin();
  while (!seesaw.begin(DEFAULT_I2C_ADDR)) {
    Serial.println(F("seesaw not found!"));
    delay(1000);
  }
  Serial.println(F("seesaw found!"));
}


int read_gearshifter() {
  int raw_val = seesaw.analogRead(ANALOGIN);
  // Serial.print(raw_val);

  if (data[0] < raw_val){
    if (raw_val < one_up_end){ shifter_no = 1; flg = "up";}
    else if (two_up_bgn < raw_val and raw_val < two_up_end){ shifter_no = 2; flg = "up";}
    else if (three_up_bgn < raw_val and raw_val < three_up_end){ shifter_no = 3; flg = "up";}
    else if (four_up_bgn < raw_val and raw_val < four_up_end){ shifter_no = 4; flg = "up";}
    else if (five_up_bgn < raw_val and raw_val < five_up_end){ shifter_no = 5; flg = "up";}
    else if (six_up_bgn < raw_val){ shifter_no = 6; flg = "up";}
    else {flg = "up";}
  } 
  else if (data[0] > raw_val){
    if (raw_val < one_down_end){ shifter_no = 1; flg = "down";}
    else if (two_down_bgn < raw_val and raw_val < two_down_end){ shifter_no = 2; flg = "down";}
    else if (three_down_bgn < raw_val and raw_val < three_down_end){ shifter_no = 3; flg = "down";}
    else if (four_down_bgn < raw_val and raw_val < four_down_end){ shifter_no = 4; flg = "down";}
    else if (five_down_bgn < raw_val and raw_val < five_down_end){ shifter_no = 5; flg = "down";}
    else if (six_down_bgn < raw_val){ shifter_no = 6; flg = "down";}
    else {flg = "down";}
  }
  else {flg = "stay";}

  // Serial.print(",\t");
  // Serial.print(data[0]);
  // Serial.print(",\t");
  // Serial.print(shifter_no);
  // Serial.print(",\t");
  // Serial.println(flg);

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
        // Serial.print("play");
        sendRequest("api",  "play");
    }
    else if (res == 202) {
        // Serial.print("pause");
        sendRequest("api",  "pause");
    }

  return true;
}


long generateRandomSequence(int length) {
    std::vector<long> sequence;
    std::uniform_int_distribution<> dis(1, 9); // Generate integers between 1 and 9
    long current_time = time(NULL);
    randomSeed(current_time);
    Serial.println("current_time: " + current_time);
    long temp = random(10);

    // Serial.print("sequence: ");
    // for (int i = 0; i < length; ++i) {
    //     long temp = random(10);
    //     sequence.push_back(temp);
    //     Serial.print(temp);
    // }
    return temp;
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
              sendRequest("nback_http", "no");
              return "no";
          }
          else{
              sendRequest("nback_http", "yes");
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



String YesOrNo_foot_button(int foot_button_pin){
  uint32_t  start_time;
  uint32_t  start_time_pressed;
  uint32_t  diff;
  uint32_t  LastTimerTick_foot_nback;


  start_time = millis();
  while (true) {

      if(! digitalRead(foot_button_pin)){  
          start_time_pressed = millis();
          while (! digitalRead(foot_button_pin)){
            Serial.print(digitalRead(foot_button_pin));
          }
          diff = millis() - start_time_pressed;
          if(diff <= 500){
              sendRequest("nback_http", "no");
              return "no";
          }
          else{
              sendRequest("nback_http", "yes");
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
  int yes_shift_no = 2;
  int no_shift_no = 4;

  while (true) {
    int yn_shift_no = read_gearshifter();
    Serial.print("yn_shift_no: ");
    Serial.println(yn_shift_no);

    if(yn_shift_no != yn_previous_shift_no){    
      if(yn_shift_no == yes_shift_no){ 
          return "yes"; 
          break;
      }
      if(yn_shift_no == no_shift_no){ 
          return "no";
          break;
      }
      else{
          if(millis() - start_time > timeout){
            return "timeout";
            // delay(700);
            break;
          } 
      }
    }
    else if (millis() - start_time > timeout){
            return "timeout";
            // delay(700);
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
              sendRequest("nback_http", "no");
              return "no";
          }
          else{
              sendRequest("nback_http", "yes");
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
    delay(400);
}

bool assert_result(int i, int prev_num, int crnt_num, String userInput){

    if (i == 1){
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
            if (crnt_num == prev_num) {
                react("correct");
                return true;
            }
            else {
                react("incorrect");
            }
        }
        else if (userInput == "no") {
            if (crnt_num != prev_num) {
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


void hexdump(const void *mem, uint32_t len, uint8_t cols = 16) {
	const uint8_t* src = (const uint8_t*) mem;
	Serial.printf("\n[HEXDUMP] Address: 0x%08X len: 0x%X (%d)", (ptrdiff_t)src, len, len);
	for(uint32_t i = 0; i < len; i++) {
		if(i % cols == 0) {
			Serial.printf("\n[0x%08X] 0x%08X: ", (ptrdiff_t)src, i);
		}
		Serial.printf("%02X ", *src);
		src++;
	}
	Serial.printf("\n");
}


void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  global_type = type;
	
  switch(type) {
		case WStype_DISCONNECTED:
			Serial.printf("[WSc] Disconnected!\n");
			break;
		case WStype_CONNECTED:
			Serial.printf("[WSc] Connected to url: %s\n", payload);

			// send message to server when Connected
			// webSocket.sendTXT("Connected");
			break;
		case WStype_TEXT:
			// Serial.printf("[WSc] get text: %s\n", payload);
      global_payload = "";
      global_payload = (char *)payload;
			// Serial.println("global_payload: " + global_payload);
      if(global_payload == "N-back: finish_nback"){
        nback_finish_flg = true;
      }

			// send message to server
			// webSocket.sendTXT("message here");
			break;
		case WStype_BIN:
			Serial.printf("[WSc] get binary length: %u\n", length);
			hexdump(payload, length);
			// send data to server
			// webSocket.sendBIN(payload, length);
			break;
		case WStype_ERROR:			
		case WStype_FRAGMENT_TEXT_START:
		case WStype_FRAGMENT_BIN_START:
		case WStype_FRAGMENT:
		case WStype_FRAGMENT_FIN:
			break;
	}
}


String YesOrNo_watch() {
	uint32_t  start_time;
  uint32_t  diff;
  String url = "/mode_server/Nback_watch";

  start_time = millis();
  
  while(true){
    webSocket.loop();
    if(global_payload == "N-back: yes"){
      Serial.println("yes");
      global_payload = "";
      return "yes"; //Buffer 59 65 73
      break;
    }
    else if(global_payload == "N-back: no"){ 
      Serial.println("no");
      return "no"; //Buffer 4e 6f
      break;
    }
    else if(millis() - start_time > timeout){
      global_payload = "";
      return "timeout";
      break;
    } 
  }
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
void nBackTask(int input_type) {

  int wholeCount = 0;
  int correctCount = 0;
  int current_num = 99;
  int previous_num = 99;
  String userInput;


  while (!nback_finish_flg){
    webSocket.loop();

    wholeCount ++;
    previous_num = current_num;
    current_num = generateRandomSequence(1);

    sendRequest("nback", String(std::to_string(current_num).c_str()));
    webSocket.loop();
    delay(300);
    webSocket.loop();

    switch (input_type)
    {
    case 0: // button
      userInput = YesOrNo_button(button);
      break;
    case 1: // gearshifter
      userInput = YesOrNo_gearshifter(seesaw);
      break;
    case 3: // foot button
      userInput = YesOrNo_foot_button(foot_button_pin);
      break;
    case 4: // throttle
      userInput = YesOrNo_throttle(throttle_pin);
      break;
    case 5: // watch
      userInput = YesOrNo_watch();
      break;
    default:
      break;
    }

    if (assert_result(wholeCount, previous_num, current_num, userInput)) {
        correctCount++;
    }

    webSocket.loop();
    delay(1000);
    webSocket.loop();
  }

    double accuracy = static_cast<double>(correctCount) / wholeCount * 100;
    Serial.print("Accuracy: " + String(accuracy));
    sendRequest("nback", "Total=" + String(wholeCount));
    sendRequest("nback", "Correct count=" + String(correctCount));
    sendRequest("nback", "Accuracy=" + String(accuracy, DEC));
    sendRequest("nback",  "end");

    nback_finish_flg = false;
}

