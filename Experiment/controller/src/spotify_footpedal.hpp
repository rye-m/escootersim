// #pragma once
// #include <WiFi.h>
// #include <network.h>
// #include <others.h>
// #include <setupFunc.h>
// #include <HTTPClient.h>
// #include <Wire.h>
// #include "Adafruit_MPR121.h"
// #include <SparkFun_Qwiic_Button.h>

// uint32_t  LastTimerTick;
const int X_pin = 32; // analog pin connected to X output


void ButtonState_footpedal(){
  static int state = 0;
  uint32_t Ti;
  static uint32_t DoubleClickTick;
  
  switch(state){
    case 0:                                             // ボタン押下チェックstate
            if(isPressed(X_pin, 1000) == true){                   // プルアップされているので押下でL
              LastTimerTick = millis();                 // 押下時の時間セット
              state = 1;
            }
            break;
    case 1:                                             // ボタン離しチェックstate
            if(isPressed(X_pin, 1000) != true){                   // 立ち上がりを検出
              Ti = millis() - LastTimerTick;
              if(Ti >= 500 ){                           // 500ms超えた？
                Serial.println("long press: previous");          // 長押し確定
                sendRequest("api",  "previous");
                state = 0;
              } else if(Ti >= 100){                     // シングルクリック仮確定
//              Serial.println("1:click!");
                DoubleClickTick =  millis();            // シングルクリック時の時間格納
                state = 2;
              }
            }
            break;
    case 2:                                             // ボタン押下チェックstate
          if(isPressed(X_pin, 1000) == true){                     // プルアップされているので押下でL
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
            if(isPressed(X_pin, 1000) != true){                   // 立ち上がりを検出
              Ti = millis() - LastTimerTick;
              if(Ti >= 500 ){                           // 500ms超えた？
                Serial.println("long press: previous");          // シングルクリック->長押し確定
                sendRequest("api",  "previous");
                state = 0;
              } else if(Ti >= 250){
                Ti = millis()-DoubleClickTick;
//              Serial.println(Ti,DEC);
                if( Ti <= 500){                         // シングルクリックから500ms以内だったら、ダブルクリック確定
                  Serial.println("Doble click: next");
                  sendRequest("api",  "next");
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

void spotify_footpedal_setup(){
  init_wifi();
  sendRequest("api",  "first_contact");
}

void spotify_footpedal_loop() {
ButtonState_footpedal();
}
