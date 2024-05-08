
// #include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include "Adafruit_MPR121.h"
#include <SparkFun_Qwiic_Button.h>
#include <network.h>

#ifndef _BV
#define _BV(bit) (1 << (bit)) 
#endif

QwiicButton button;
uint8_t brightness = 100;   //The brightness to set the LED to when the button is pushed
                            //Can be any value between 0 (off) and 255 (max)
// const char *ssid = "deviceFarm";
// const char *password = "device@theFarm";
const int sequenceLength = 10;
const int n = 1;
const int timeout = 4000;
int sendRequest(String);


// put function definitions here:
// int sendRequest(String command) {
//   // Conect to the WiFi
//   HTTPClient http;

//   String serverPath = "http://192.168.0.153:8888/nback";
//   // Serial.print("URL: ");  Serial.print(serverPath);
//   // Serial.print(",\tcommand: ");  Serial.println(command);
//   // Your Domain name with URL path or IP address with path
//   http.begin(serverPath.c_str());
  
//   // If you need Node-RED/server authentication, insert user and password below
//   //http.setAuthorization("REPLACE_WITH_SERVER_USERNAME", "REPLACE_WITH_SERVER_PASSWORD");
  
//   // Specify content-type header
//   http.addHeader("Content-Type", "application/json");

//   // Data to send with HTTP POST
//   String httpRequestData = "{\"command\":\"" + command + "\"}";

//   // Send HTTP POST request
//   int httpResponseCode = http.POST(httpRequestData);
  
//   if (httpResponseCode == 200) {
//     // Serial.print("HTTP Response code: "); Serial.println(httpResponseCode);
//   }
//   else {
//     Serial.print("Error code: ");
//     Serial.println(httpResponseCode);
//   }
//   // Free resources
//   http.end();

//   return httpResponseCode;
// }


// Function to generate a random sequence of integers
std::vector<int> generateRandomSequence(int length) {
    std::vector<int> sequence;
    std::uniform_int_distribution<> dis(1, 9); // Generate integers between 1 and 9
    
    Serial.print("sequence: ");
    for (int i = 0; i < length; ++i) {
        int temp = rand() % 10;
        sequence.push_back(temp);
        Serial.print(temp);
    }
      Serial.println("");
    return sequence;
}


String ButtonState(){
  uint32_t  start_time;
  uint32_t  start_time_pressed;
  uint32_t  diff;

  start_time = millis();
  while (true) {
      if(button.isPressed()){  
          start_time_pressed = millis();
          button.LEDon(100);
          while (button.isPressed()){
            // Serial.print(".");
          }
          button.LEDoff();
          diff = millis() - start_time_pressed;
          if(diff <= 500){
              Serial.println("yes");
              return "yes";
          }
          else{
              Serial.println("no");
              return "no";
          }
          break;
      }
      else{
          if(millis() - start_time > timeout){
            return "timeout";
            break;
          } 
      }
  }            
}

void react(String answer){
    sendRequest(answer);
    Serial.println(answer);
    delay(300);
}


// Function to run the N-back task
void nBackTask(const std::vector<int>& sequence, int n) {

    int correctCount = 0;
    int totalTrials = 0;
    String userInput;

    for (int i = 0; i < sequence.size(); ++i) {
        sendRequest(String(std::to_string(sequence[i]).c_str()));
        Serial.println("\n\"" + String(std::to_string(sequence[i]).c_str()) + "\"");
        delay(100);
        Serial.print("Match? -> ");
        userInput = ButtonState();

        if (i - n < 0){
            if (userInput == "yes"){
                react("incorrect");
            }
            else if (userInput == "no"){
                react("correct");
                correctCount++;
            }
            else if (userInput == "timeout") {
                Serial.println("Time out");
                }
            else {
                Serial.println("Invalid input! Please enter 'y' or 'n'.");
            }
        }
        else{
            if (userInput == "yes") {
                if (sequence[i] == sequence[i - n]) {
                    react("correct");
                    correctCount++;
                }
                else {
                    react("incorrect");
                }
            }
            else if (userInput == "no") {
                if (sequence[i] != sequence[i - n]) {
                    react("correct");
                    correctCount++;
                }
                else {
                    react("incorrect");
                }
            }
            else if (userInput == "timeout") {
                Serial.println("Time out");
                }
            else {
                Serial.println("Invalid input! Please enter 'y' or 'n'.");
            }
        }

        totalTrials++;
        delay(1000);
    }

    double accuracy = static_cast<double>(correctCount) / totalTrials * 100;
    Serial.print("Accuracy: ");
    Serial.print(accuracy);
    Serial.print("%");
    sendRequest(String(accuracy, DEC));
    sendRequest("end");
}


void setup(){
    Serial.begin(115200);
    delay(1000);

    WiFi.mode(WIFI_STA); //Optional
    WiFi.begin(ssid, password);
    Serial.println("\nConnecting");

    while(WiFi.status() != WL_CONNECTED){
        Serial.print(".");
        delay(100);
    }

    Serial.println("\nConnected to the WiFi network");
    Serial.print("Local TinyPICO IP: ");
    Serial.println(WiFi.localIP());

  delay(1000);
    
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

  sendRequest("connected");
}


void loop() {

    if(button.isPressed() == true){
      sendRequest("begin");
      delay(2000);
      std::vector<int> sequence = generateRandomSequence(sequenceLength);
      nBackTask(sequence, n);
      delay(60000);
    }


}