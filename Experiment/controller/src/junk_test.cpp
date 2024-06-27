#include <seesaw_neopixel.h>
#include "Adafruit_MPR121.h"
#include <SparkFun_Qwiic_Button.h>
#include <seesaw_neopixel.h>
#include <WiFiClientSecure.h>
#include <WebSocketsClient.h>

#define SECONDARY_I2C_PORT &Wire1
#define  DEFAULT_I2C_ADDR 0x30
#define  ANALOGIN   18

Adafruit_seesaw seesaw(&Wire1);

const int sequenceLength = 10;
const int n = 1;
const int timeout = 3000;
const int foot_button_pin = A1; // analog pin connected to X output
const int throttle_pin = A2; // analog pin connected to X output
const int throttle_th = 2900; // thrashhold for the potentiometer of the throttle

uint8_t brightness = 100;   //The brightness to set the LED to when the button is pushed
uint8_t yes[3] = {0x59, 0x65, 0x73};
uint8_t no[2] = {0x4e, 0x65};
String global_payload = "";


String flg;
int shifter_no;
int data[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int new_data[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int previous_shift_no = 99;

int one_up_bgn = 910;
int one_up_end = 926;
int two_up_bgn = 812;
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
int two_down_bgn = 850;
int two_down_end = 871;
int three_down_bgn = 782;
int three_down_end = 812;
int four_down_bgn = 730;
int four_down_end = 764;
int five_down_bgn = 676;
int five_down_end = 704;
int six_down_bgn = 601;
int six_down_end = 612;


void setup() {

  Serial.begin(115200);
  while (!Serial) delay(10);   // wait until serial port is opened
  delay(3000);

  Serial.println(F("Adafruit PID 5295 I2C QT Slide Potentiometer test!"));
  delay(1000);

  Wire1.begin();
  while (!seesaw.begin(DEFAULT_I2C_ADDR)) {
    Serial.println(F("seesaw not found!"));
    delay(1000);
  }
  delay(500);
  Serial.println(F("seesaw found!"));
}


void loop() {
  int raw_val = seesaw.analogRead(ANALOGIN);
//   Serial.println(raw_val);

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
}
