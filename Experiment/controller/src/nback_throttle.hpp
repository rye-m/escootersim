void nback_throttle_setup(){

  pinMode(throttle_pin, INPUT_PULLUP);  // set our pin to an input with a pullup resistor

  //check if button will acknowledge over I2C
  if (! isPressed(throttle_pin, throttle_th)) {
    Serial.println("Device did not acknowledge! Freezing.");
  }
  Serial.println("Device acknowledged.");

  sendRequest("nback",  "connected");
}


void nback_throttle_loop() {

  while (true){
    webSocket.loop();
    if (global_payload == "start_nback"){
      sendRequest("nback",  "begin");
      delay(2000);
      nBackTask(4);
      break;
    }
  }
}