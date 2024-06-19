#define  DEFAULT_I2C_ADDR 0x30
#define  ANALOGIN   18


void nback_gearshifter_setup(){  
  Wire1.begin();
  if (!seesaw.begin()) {
    Serial.println(F("seesaw not found!"));
    while(1) delay(10);
  }
  sendRequest("nback",  "nback_gearshifter_connected");
}


void nback_gearshifter_loop() {
    int shift_no = read_gearshifter()
    if(shift_no == 1){
      sendRequest("nback",  "begin");
      delay(2000);
      std::vector<int> sequence = generateRandomSequence(sequenceLength);
      nBackTask(sequence, n, 1);
      delay(120000);
    }


}