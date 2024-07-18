uint32_t  gearshifter_spotify_timeout = 500;

// // const int X_pin = 32; // analog pin connected to X output
void navi_gearshifter_setup() {
  gearshifter_setup();
  sendRequest("api",  "navi_gearshifter_connected");
}


void navi_gearshifter_loop() {
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
              Serial.println("Gear: 1 show/hide ETA");
              sendRequest("navi",  "ETA");
            break;
          case 2:
              Serial.println("Gear: 2 'STAY' (doesn't do anything)");
            break;
          case 3:
              Serial.println("Gear: 3 'zoom in/out'");
              sendRequest("navi",  "zoom");
            break;
          case 4:
              Serial.println("Gear: 4 doesn't do anything");
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