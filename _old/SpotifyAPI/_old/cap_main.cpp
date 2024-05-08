// #include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include "Adafruit_MPR121.h"

#ifndef _BV
#define _BV(bit) (1 << (bit)) 
#endif

// You can have up to 4 on one i2c bus but one is enough for testing!
Adafruit_MPR121 cap = Adafruit_MPR121();

// Keeps track of the last pins touched
// so we know when buttons are 'released'
uint16_t lasttouched = 0;
uint16_t currtouched = 0;

const char *ssid = "deviceFarm";
const char *password = "device@theFarm";


// put function definitions here:
bool sendRequest(String command) {
  // Conect to the WiFi
  HTTPClient http;

  String serverPath = "http://192.168.0.153:8888/api";
  Serial.print("URL: ");  Serial.print(serverPath);
  Serial.print(",\tcommand: ");  Serial.println(command);
  // Your Domain name with URL path or IP address with path
  http.begin(serverPath.c_str());
  
  // If you need Node-RED/server authentication, insert user and password below
  //http.setAuthorization("REPLACE_WITH_SERVER_USERNAME", "REPLACE_WITH_SERVER_PASSWORD");
  
  // Specify content-type header
  http.addHeader("Content-Type", "application/json");

  // Data to send with HTTP POST
  String httpRequestData = "{\"command\":\"" + command + "\"}";

  // Send HTTP POST request
  int httpResponseCode = http.POST(httpRequestData);
  
  if (httpResponseCode == 200) {
    Serial.print("HTTP Response code: "); Serial.println(httpResponseCode);
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  // Free resources
  http.end();

  return true;
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

  delay(3000);
    
  // while (!Serial) { // needed to keep leonardo/micro from starting too fast!
  //   delay(10);
  // }
  
  Serial.println("Adafruit MPR121 Capacitive Touch sensor test"); 
  
  // Default address is 0x5A, if tied to 3.3V its 0x5B
  // If tied to SDA its 0x5C and if SCL then 0x5D
  if (!cap.begin(0x5A)) {
    Serial.println("MPR121 not found, check wiring?");
    while (1);
  }
  Serial.println("MPR121 found!");

  sendRequest("first_contact");
}


void loop() {
  // Get the currently touched pads
  currtouched = cap.touched();
  
  for (uint8_t i=0; i<12; i++) {
    // it if *is* touched and *wasnt* touched before, alert!
    if ((currtouched & _BV(i)) && !(lasttouched & _BV(i)) ) {

      if (i == 0) {sendRequest("previous");}
      else if (i == 11) {sendRequest("next");}
      else if (i == 5) {sendRequest("play");}
      else if (i == 6) {sendRequest("pause");}
    }
    // if it *was* touched and now *isnt*, alert!
    if (!(currtouched & _BV(i)) && (lasttouched & _BV(i)) ) {
      //Serial.print(i); Serial.println(" released");
    }
  }

  // reset our state
  lasttouched = currtouched;

  // comment out this line for detailed data from the sensor!
  return;
  
  // debugging info, what
  Serial.print("\t\t\t\t\t\t\t\t\t\t\t\t\t 0x"); Serial.println(cap.touched(), HEX);
  Serial.print("Filt: ");
  for (uint8_t i=0; i<12; i++) {
    Serial.print(cap.filteredData(i)); Serial.print("\t");
  }
  Serial.println();
  Serial.print("Base: ");
  for (uint8_t i=0; i<12; i++) {
    Serial.print(cap.baselineData(i)); Serial.print("\t");
  }
  Serial.println();
  
  // put a delay so it isn't overwhelming
  delay(100);
}

// #include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include "Adafruit_MPR121.h"
#include <SparkFun_Qwiic_Button.h>

#ifndef _BV
#define _BV(bit) (1 << (bit)) 
#endif

QwiicButton button1;
QwiicButton button2;

const char *ssid = "deviceFarm";
const char *password = "device@theFarm";


// put function definitions here:
bool sendRequest(String command) {
  // Conect to the WiFi
  HTTPClient http;

  String serverPath = "http://192.168.0.153:8888/api";
  Serial.print("URL: ");  Serial.print(serverPath);
  Serial.print(",\tcommand: ");  Serial.println(command);
  // Your Domain name with URL path or IP address with path
  http.begin(serverPath.c_str());
  
  // If you need Node-RED/server authentication, insert user and password below
  //http.setAuthorization("REPLACE_WITH_SERVER_USERNAME", "REPLACE_WITH_SERVER_PASSWORD");
  
  // Specify content-type header
  http.addHeader("Content-Type", "application/json");

  // Data to send with HTTP POST
  String httpRequestData = "{\"command\":\"" + command + "\"}";

  // Send HTTP POST request
  int httpResponseCode = http.POST(httpRequestData);
  
  if (httpResponseCode == 200) {
    Serial.print("HTTP Response code: "); Serial.println(httpResponseCode);
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  // Free resources
  http.end();

  return true;
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

  //check if the buttons will acknowledge over I2C
  //connect to Qwiic button at address 0x5B
  if (button1.begin(0x5B) == false){
    Serial.println("Button 1 did not acknowledge! Freezing.");
    while(1);
  }
  //connect to Qwiic button at default address, 0x6F
  if (button2.begin() == false) {
    Serial.println("Button 2 did not acknowledge! Freezing.");
    while(1);
  }
  Serial.println("Both buttons acknowledged.");

  sendRequest("first_contact");
}


void loop() {
  // Get the currently touched pads
  //check if button 1 is pressed, and tell us if it is!
  if (button1.isPressed() == true) {
    Serial.println("Button 1 is pressed!");
    while (button1.isPressed() == true)
      delay(10);  //wait for user to stop pressing
    Serial.println("Button 1 is not pressed.");
  }

  //check if button 2 is pressed, and tell us if it is!
  if (button2.isPressed() == true){
    Serial.println("Button 2 is pressed!");
    while (button2.isPressed() == true)
      delay(10);  //wait for user to stop pressing
    Serial.println("Button 2 is not pressed.");
  }
  delay(20); //Don't hammer too hard on the I2C bus.
}

