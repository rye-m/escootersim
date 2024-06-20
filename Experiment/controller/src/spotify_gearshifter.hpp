#include <Arduino.h>

// // const int X_pin = 32; // analog pin connected to X output
void spotify_gearshifter_setup() {
  gearshifter_setup();
  sendRequest("api",  "spotify_gearshifter_connected");
}


void spotify_gearshifter_loop() {
  int shift_no = read_gearshifter();
    if(shift_no == previous_shift_no){
      previous_shift_no = shift_no;
    }
    else{
      switch (shift_no)
        {
        case 1: // gearshifter
            Serial.println("next");
            sendRequest("api",  "next");
          break;
        case 2:
            sendRequest("api",  "play");
            Serial.println("play");
          break;
        case 3:
            Serial.println("pause");
            sendRequest("api",  "pause");
          break;
        case 4:
            Serial.println("previous");
            sendRequest("api",  "previous");
          break;
        case 5:
            Serial.println("Gear: 5 doesn't do anything");
          break;
        case 6:
            Serial.println("Gear: 6 doesn't do anything");
          break;
        
        default:
          break;
        }  
      delay(50);
      previous_shift_no = shift_no;
    }
}