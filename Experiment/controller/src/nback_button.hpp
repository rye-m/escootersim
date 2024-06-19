void nback_button_setup(){

  Serial.println("Qwiic button examples");
  Wire1.begin(); //Join I2C bus

  //check if button will acknowledge over I2C
  if (button.begin(0x6F, Wire1) == false) {
    Serial.println("Device did not acknowledge! Freezing.");
    while (1);
  }
  Serial.println("Button acknowledged.");

  //Start with the LED off
  button.LEDoff();

  sendRequest("nback",  "connected");
}


void nback_button_loop() {

    if(button.isPressed() == true){
      sendRequest("nback",  "begin");
      delay(2000);
      std::vector<int> sequence = generateRandomSequence(sequenceLength);
      nBackTask(sequence, n, 0);
      delay(60000);
    }


}