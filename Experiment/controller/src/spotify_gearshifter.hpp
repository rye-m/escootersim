// #include <WiFi.h>
// #include <network.h>
// #include <others.h>
// #include <setupFunc.h>
// #include <HTTPClient.h>
// #include <Wire.h>
// #include "Adafruit_MPR121.h"
// #include <SparkFun_Qwiic_Button.h>
// #include <seesaw_neopixel.h>

#define  DEFAULT_I2C_ADDR 0x30
#define  ANALOGIN   18
#define  NEOPIXELOUT 14

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
  init_wifi();
  
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

    for (uint8_t i=0; i< pixels.numPixels(); i++) {
        pixels.setPixelColor(i, Wheel(slide_val / 4));
        }
        pixels.show();
  
  delay(50);
}