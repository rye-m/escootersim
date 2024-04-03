
// #include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include "Adafruit_MPR121.h"
#include <SparkFun_Qwiic_Button.h>

uint32_t  LastTimerTick;
const char *ssid = "deviceFarm";
const char *password = "device@theFarm";
const int X_pin = 32; // analog pin connected to X output


// put function definitions here:
int sendRequest(String command) {
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

  return httpResponseCode;
}

bool playOrPause() {

    int res = sendRequest("currently-playing");
    
    if (res == 201) {
        Serial.print("play");
        sendRequest("play");
    }
    else if (res == 202) {
        Serial.print("pause");
        sendRequest("pause");
    }

  return true;
}

bool isPressed(){
  int deg = analogRead(X_pin);
  if (deg > 1000) {
    return true;
  }
  else {
    return false;
  }
}

void ButtonState(){
  static int state = 0;
  uint32_t Ti;
  static uint32_t DoubleClickTick;
  
  switch(state){
    case 0:                                             // ボタン押下チェックstate
            if(isPressed() == true){                   // プルアップされているので押下でL
              LastTimerTick = millis();                 // 押下時の時間セット
              state = 1;
            }
            break;
    case 1:                                             // ボタン離しチェックstate
            if(isPressed() != true){                   // 立ち上がりを検出
              Ti = millis() - LastTimerTick;
              if(Ti >= 500 ){                           // 500ms超えた？
                Serial.println("long press: previous");          // 長押し確定
                sendRequest("previous");
                state = 0;
              } else if(Ti >= 100){                     // シングルクリック仮確定
//              Serial.println("1:click!");
                DoubleClickTick =  millis();            // シングルクリック時の時間格納
                state = 2;
              }
            }
            break;
    case 2:                                             // ボタン押下チェックstate
          if(isPressed() == true){                     // プルアップされているので押下でL
              LastTimerTick = millis();                 // 押下時の時間セット
              state = 3;
            }
            if( millis()-DoubleClickTick >= 500){       // シングルクリック確定
                Serial.println("click: play/puase");
                playOrPause();
                state = 0;
            }
            break;
    case 3:                                             // ボタン離しチェックstate
            if(isPressed() != true){                   // 立ち上がりを検出
              Ti = millis() - LastTimerTick;
              if(Ti >= 500 ){                           // 500ms超えた？
                Serial.println("long press: previous");          // シングルクリック->長押し確定
                sendRequest("previous");
                state = 0;
              } else if(Ti >= 250){
                Ti = millis()-DoubleClickTick;
//              Serial.println(Ti,DEC);
                if( Ti <= 500){                         // シングルクリックから500ms以内だったら、ダブルクリック確定
                  Serial.println("Doble click: next");
                  sendRequest("next");
                  state = 0;
                } else {
                  Serial.println("2:click!");           // 
                  state = 0;                  
              }
            }
            break;
    default:
          break;
    }
  }            
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

  sendRequest("first_contact");
}

void loop() {
ButtonState();
}
