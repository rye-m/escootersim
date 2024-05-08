
// #include <Arduino.h>
#include <WiFi.h>
#include <network.h>
#include <HTTPClient.h>
#include <Wire.h>
#include "Adafruit_MPR121.h"
#include <SparkFun_Qwiic_Button.h>

#ifndef _BV
#define _BV(bit) (1 << (bit)) 
#endif

QwiicButton button1;
QwiicButton button2;
uint32_t  LastTimerTick;
QwiicButton button;
uint8_t brightness = 100;   //The brightness to set the LED to when the button is pushed
                            //Can be any value between 0 (off) and 255 (max)

// put function definitions here:
int sendRequest(String);

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

void ButtonState(){
  static int state = 0;
  uint32_t Ti;
  static uint32_t DoubleClickTick;
  
  switch(state){
    case 0:                                             // ボタン押下チェックstate
            if(button.isPressed() == true){                   // プルアップされているので押下でL
              LastTimerTick = millis();                 // 押下時の時間セット
              state = 1;
              button.LEDon(100);
            }
            break;
    case 1:                                             // ボタン離しチェックstate
            if(button.isPressed() != true){                   // 立ち上がりを検出
              Ti = millis() - LastTimerTick;
              button.LEDoff();
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
          if(button.isPressed() == true){                     // プルアップされているので押下でL
              LastTimerTick = millis();                 // 押下時の時間セット
              state = 3;
              button.LEDon(100);
            }
            if( millis()-DoubleClickTick >= 500){       // シングルクリック確定
                Serial.println("click: play/puase");
                playOrPause();
                state = 0;
            }
            break;
    case 3:                                             // ボタン離しチェックstate
            if(button.isPressed() != true){                   // 立ち上がりを検出
              Ti = millis() - LastTimerTick;
              button.LEDoff();
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

  sendRequest("first_contact");
}


void loop() {
  ButtonState();
  }