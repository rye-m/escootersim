void nback_gearshifter_setup(){  
  gearshifter_setup();
  sendRequest("nback",  "nback_gearshifter_connected");
}


void nback_gearshifter_loop() {
    int shift_no = read_gearshifter();

    if(shift_no == previous_shift_no){
      previous_shift_no = shift_no;
    }
    else{
      if(shift_no == 3){
        sendRequest("nback",  "begin");
        delay(2000);
        std::vector<int> sequence = generateRandomSequence(sequenceLength);
        nBackTask(sequence, n, 1);
        delay(120000);
      }

    }


}