// #include <Arduino.h>
// #include <SparkFun_Qwiic_Button.h>
// QwiicButton button;

// void setup() {
//   Serial.begin(115200);
//   delay(2000);
//   Serial.println("Qwiic button examples");
//   Wire1.begin(); //Join I2C bus
//   delay(3000);

//   Wire1.setPins(SDA1, SCL1);
//   delay(2000);

//   //check if button will acknowledge over I2C
//   if (button.begin() == false) {
//     Serial.println("Device did not acknowledge! Freezing.");
//     while(1) delay(10);
//   }
//   Serial.println("Button acknowledged.");
// }

// void loop() {
//   //check if button is pressed, and tell us if it is!
//   if (button.isPressed() == true) {
//     Serial.println("The button is pressed!");
//     while (button.isPressed() == true)
//       delay(10);  //wait for user to stop pressing
//     Serial.println("The button is not pressed!");
//   }
//   delay(20); //Don't hammer too hard on the I2C bus
// }

#include <seesaw_neopixel.h>
#include <Arduino.h>
#include <Wire.h>
#include <SparkFun_Qwiic_Button.h>

#define  DEFAULT_I2C_ADDR 0x30
#define  ANALOGIN   18
Adafruit_seesaw seesaw;
QwiicButton button;

String flg;
int shifter_no;
int data[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int new_data[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

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


void setup() {
  Serial.begin(115200);
  Serial.println("Qwiic button examples");
  Wire.begin(); //Join I2C bus

  //check if button will acknowledge over I2C
  if (button.begin() == false) {
    Serial.println("Device did not acknowledge! Freezing.");
    while (1);
  }
  Serial.println("Button acknowledged.");

  //Start with the LED off
  button.LEDoff();


  Wire.begin();
  if (!seesaw.begin(DEFAULT_I2C_ADDR)) {
    Serial.println(F("seesaw not found!"));
    while(1) delay(10);
  }
  delay(500);
  Serial.println(F("seesaw found!"));
}

void loop() {
  int raw_val = seesaw.analogRead(ANALOGIN);
  int mapped_val = map(seesaw.analogRead(ANALOGIN), 0, 1023, 1, 3);
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


  // button.LEDon();
  // delay(250); // wait 3 seconds
  // button.LEDoff();
  // delay(250); // wait 3 seconds
}
