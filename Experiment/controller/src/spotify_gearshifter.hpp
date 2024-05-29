#include <Arduino.h>

#define  DEFAULT_I2C_ADDR 0x30
#define  ANALOGIN   18

int next_e = 60;
int play_b = 230;
int play_e = 370;
int pause_b = 400;
int pause_e = 710;
int previous_b = 720;


// // const int X_pin = 32; // analog pin connected to X output
String current_input = "none";
String previous_input = "pause";


void spotify_gearshifter_setup() {
  Wire.begin();
  if (!seesaw.begin(DEFAULT_I2C_ADDR)) {
    Serial.println(F("seesaw not found!"));
    while(1) delay(10);
  }
  sendRequest("api",  "spotify_gearshifter_connected");
}


void spotify_gearshifter_loop() {
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

  
  delay(50);
}