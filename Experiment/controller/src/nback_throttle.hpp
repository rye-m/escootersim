void nback_throttle_setup(){

  pinMode(throttle_pin, INPUT_PULLUP);  // set our pin to an input with a pullup resistor

  //check if button will acknowledge over I2C
  if (! isPressed(throttle_pin, throttle_th)) {
    Serial.println("Device did not acknowledge! Freezing.");
  }
  Serial.println("Device acknowledged.");

  sendRequest("printout",  "nback_throttle_connected");
}


void nback_throttle_loop() {
  if (global_payload == "N-back: start_nback"){
    sendRequest("nback",  "begin");
    delay(2000);
    global_payload = "";
    nBackTask(4);
  }
}