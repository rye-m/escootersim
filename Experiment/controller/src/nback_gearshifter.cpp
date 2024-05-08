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

Adafruit_seesaw seesaw;
seesaw_NeoPixel pixels = seesaw_NeoPixel(4, NEOPIXELOUT, NEO_GRB + NEO_KHZ800);

// const int X_pin = 32; // analog pin connected to X output
int previous_input = 0;


// Function to run the N-back task
void nBackTask(const std::vector<int>& sequence, int n) {

    int correctCount = 0;
    String userInput;

    for (int i = 0; i < sequence.size(); ++i) {
        sendRequest("nback", String(std::to_string(sequence[i]).c_str()));
        Serial.println("\n\"" + String(std::to_string(sequence[i]).c_str()) + "\"");
        delay(100);
        Serial.print("Match? -> ");
        userInput = YesOrNo_button(button);

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


void setup(){
  init_wifi();

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

  sendRequest("nback",  "first_contact");
}


void loop() {

    if(button.isPressed() == true){
      sendRequest("nback",  "begin");
      delay(2000);
      std::vector<int> sequence = generateRandomSequence(sequenceLength);
      nBackTask(sequence, n);
      delay(60000);
    }


}