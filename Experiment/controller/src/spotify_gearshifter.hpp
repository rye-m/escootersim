uint32_t  gearshifter_spotify_timeout = 500;

// // const int X_pin = 32; // analog pin connected to X output
void spotify_gearshifter_setup() {
  gearshifter_setup();
  sendRequest("api",  "spotify_gearshifter_connected");
}


void spotify_gearshifter_loop() {
  int shift_no = read_gearshifter();
  uint32_t start_time;
  
  if(shift_no != previous_shift_no){
    int latest_shift_no;
    start_time = millis();
    while(true){
      latest_shift_no = read_gearshifter();
      if(latest_shift_no != shift_no){
        shift_no = latest_shift_no;
      }
      if((millis() - start_time) >= gearshifter_spotify_timeout){
        switch (shift_no)
          {
          case 1: // gearshifter
              Serial.println("play 1st song");
              sendRequest("gearshifter",  "0");
            break;
          case 2:
              Serial.println("play 2nd song");
              sendRequest("gearshifter",  "1");
            break;
          case 3:
              Serial.println("play 3rd song");
              sendRequest("gearshifter",  "2");
            break;
          case 4:
              Serial.println("play 4th song");
              sendRequest("gearshifter",  "3");
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

        previous_shift_no = shift_no;
        break;
      }
    }
  }
  else{
    previous_shift_no = shift_no;
    Serial.print("shift_no: ");
    Serial.print(shift_no);
    Serial.print(",\tprevious_shift_no: ");
    Serial.println(previous_shift_no);
  }
}