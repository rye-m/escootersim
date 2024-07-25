// #include <WiFi.h>
// #include <network.h>
// #include <others.h>
// #include <setupFunc.h>
// #include <HTTPClient.h>
// #include <Wire.h>
// #include "Adafruit_MPR121.h"
// #include <SparkFun_Qwiic_Button.h>


// Function to run the N-back task
// void nBackTask(const std::vector<int>& sequence, int n) {

//     int correctCount = 0;
//     String userInput;

//     for (int i = 0; i < sequence.size(); ++i) {
//         sendRequest("nback", String(std::to_string(sequence[i]).c_str()));
//         Serial.println("\n\"" + String(std::to_string(sequence[i]).c_str()) + "\"");
//         delay(100);
//         Serial.print("Match? -> ");
//         userInput = YesOrNo_button(button);

//         if (assert_result(i, sequence, userInput)) {
//             correctCount++;
//         }
//         delay(1000);
//     }

//     double accuracy = static_cast<double>(correctCount) / sequenceLength * 100;
//     Serial.print("Accuracy: ");
//     Serial.print(accuracy);
//     sendRequest("nback", String(accuracy, DEC));
//     sendRequest("nback",  "end");
// }


void nback_footpedal_setup(){
  init_wifi();

  Serial.println("Qwiic button examples");
  Wire.begin(); //Join I2C bus

  //check if button will acknowledge over I2C
  if (button.begin() == false) {
    Serial.println("Device did not acknowledge! Freezing.");
    while (1);
  }
  Serial.println("Button acknowledged.");

  //Start with the LED off
  button.LEDoff();

  sendRequest("nback",  "connected");
}


void nback_footpedal_loop() {
	delay(10000);

  sendRequest("nback",  "begin");
  delay(2000);
  std::vector<long> sequence = generateRandomSequence(sequenceLength);
  nBackTask(sequence, n, 3);
  delay(300000);

}