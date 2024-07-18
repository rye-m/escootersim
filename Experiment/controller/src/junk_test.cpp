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


// int one_up_bgn = 0;
// int one_up_end = 0;
// int two_up_bgn = 1;
// int two_up_end = 95;
// int three_up_bgn = 102;
// int three_up_end = 152;
// int four_up_bgn = 156;
// int four_up_end = 204;
// int five_up_bgn = 214;
// int five_up_end = 265;
// int six_up_bgn = 274;
// int six_up_end = 371;
// int one_down_bgn = 16;
// int one_down_end = 32;
// int two_down_bgn = 112;
// int two_down_end = 125;
// int three_down_bgn = 170;
// int three_down_end = 184;
// int four_down_bgn = 228;
// int four_down_end = 240;
// int five_down_bgn = 284;
// int five_down_end = 295;
// int six_down_bgn = 348;
// int six_down_end = 372;

// int one_up_bgn = 16;
// int one_up_end = 32;
// int two_up_bgn = 112;
// int two_up_end = 125;
// int three_up_bgn = 170;
// int three_up_end = 184;
// int four_up_bgn = 228;
// int four_up_end = 240;
// int five_up_bgn = 284;
// int five_up_end = 295;
// int six_up_bgn = 348;
// int six_up_end = 372;
// int one_down_bgn = 0;
// int one_down_end = 0;
// int two_down_bgn = 1;
// int two_down_end = 95;
// int three_down_bgn = 102;
// int three_down_end = 152;
// int four_down_bgn = 156;
// int four_down_end = 204;
// int five_down_bgn = 214;
// int five_down_end = 265;
// int six_down_bgn = 274;
// int six_down_end = 371;

void setup() {

  Serial.begin(115200);
  while (!Serial) delay(10);   // wait until serial port is opened
  delay(1000);

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
  Serial.print(raw_val);

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


// void setup() {
//   Serial.begin(115200);

//   while (!Serial) delay(10);   // wait until serial port is opened
//   delay(3000);

//   Serial.println(F("Adafruit PID 5295 I2C QT Slide Potentiometer test!"));

//   Wire1.begin();
//   if (!seesaw.begin(DEFAULT_I2C_ADDR)) {
//     Serial.println(F("seesaw not found!"));
//     while(1) delay(10);
//   }

//   Serial.println(F("seesaw started OK!"));
// }



// void loop() {
//   // read the potentiometer
//   uint16_t slide_val = seesaw.analogRead(ANALOGIN);
//   Serial.println(slide_val);

//   delay(50);
// }