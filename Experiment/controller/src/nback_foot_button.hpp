// const int input_pin = 23; // analog pin connected to X output


void nback_foot_button_setup(){
  pinMode(foot_button_pin, INPUT_PULLUP);  // set our pin to an input with a pullup resistor

  //check if button will acknowledge over I2C
  if (digitalRead(foot_button_pin)) {
    Serial.println("Foot button acknowledged.");
  }

  sendRequest("printout",  "nback_footbutton_connected");
}


void nback_foot_button_loop() {
  if (global_payload == "N-back: start_nback"){
    sendRequest("nback",  "begin");
    delay(3000);
    global_payload = "";
    nBackTask(3);
  }
}
