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
	delay(10000);

  sendRequest("nback",  "begin");
  delay(2000);
  std::vector<long> sequence = generateRandomSequence(sequenceLength);
  nBackTask(sequence, n, 4);
  delay(300000);


}