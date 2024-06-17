#define  DEFAULT_I2C_ADDR 0x30
#define  ANALOGIN   18


void nback_gearshifter_setup(){  
  Wire.begin();
  if (!seesaw.begin(DEFAULT_I2C_ADDR)) {
    Serial.println(F("seesaw not found!"));
    while(1) delay(10);
  }
  sendRequest("nback",  "nback_gearshifter_connected");
}


void nback_gearshifter_loop() {
    int mapped_val = map(seesaw.analogRead(ANALOGIN), 0, 1023, 1, 3);
    Serial.println(mapped_val);
    if(mapped_val == 1){
      sendRequest("nback",  "begin");
      delay(2000);
      std::vector<int> sequence = generateRandomSequence(sequenceLength);
      nBackTask(sequence, n, 1);
      delay(120000);
    }


}