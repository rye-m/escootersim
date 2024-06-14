// const int input_pin = 23; // analog pin connected to X output


void nback_foot_button_setup(){

  pinMode(foot_button_pin, INPUT_PULLUP);  // set our pin to an input with a pullup resistor

  //check if button will acknowledge over I2C
  if (digitalRead(foot_button_pin)) {
    Serial.println("Device did not acknowledge! Freezing.");
  }
  Serial.println("Button acknowledged.");

  sendRequest("nback",  "connected");
}


void nback_foot_button_loop() {

    if(! digitalRead(foot_button_pin)){
      sendRequest("nback",  "begin");
      delay(2000);
      std::vector<int> sequence = generateRandomSequence(sequenceLength);
      nBackTask(sequence, n, 3);
      delay(60000);
    }


}