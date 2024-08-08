// #include <Adafruit_NeoPixel.h>

uint32_t  LastTimerTick_foot;


void ButtonState_foot_button(){
  static int state = 0;
  uint32_t Ti;
  static uint32_t DoubleClickTick;
  
  switch(state){
    case 0:                                             // ボタン押下チェックstate
            if(! digitalRead(foot_button_pin)){                   // プルアップされているので押下でL
              LastTimerTick_foot = millis();                 // 押下時の時間セット
              state = 1;
            }
            break;
    case 1:                                             // ボタン離しチェックstate
            if(digitalRead(foot_button_pin)){                   // 立ち上がりを検出
              Ti = millis() - LastTimerTick_foot;
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
          if(! digitalRead(foot_button_pin)){                     // プルアップされているので押下でL
              LastTimerTick_foot = millis();                 // 押下時の時間セット
              state = 3;
            }
            if( millis()-DoubleClickTick >= 500){       // シングルクリック確定
                Serial.println("Doble click: next");
                sendRequest("api",  "next");
                state = 0;
            }
            break;
    case 3:                                             // ボタン離しチェックstate
            if(digitalRead(foot_button_pin)){                   // 立ち上がりを検出
              Ti = millis() - LastTimerTick_foot;
              if(Ti >= 500 ){                           // 500ms超えた？
                Serial.println("long press: previous");          // シングルクリック->長押し確定
                sendRequest("api",  "previous");
                state = 0;
              } else if(Ti >= 250){
                Ti = millis()-DoubleClickTick;
//              Serial.println(Ti,DEC);
                if( Ti <= 500){                         // シングルクリックから500ms以内だったら、ダブルクリック確定
                  // Serial.println("Doble click: next");
                  // sendRequest("api",  "next");
                  state = 0;
                } else {
                  Serial.println("Doble click: next");
                  sendRequest("api",  "next");
                  state = 0;                  
              }
            }
            break;
    default:
          break;
    }

  }            
}

void spotify_foot_button_setup(){
  pinMode(foot_button_pin, INPUT_PULLUP);  // set our pin to an input with a pullup resistor

  if (digitalRead(foot_button_pin)) {
    Serial.println("Device acknowledged.");
  }

  sendRequest("printout",  "spotify_foot_button_connected");
}


void spotify_foot_button_loop() {
  Serial.println(digitalRead(foot_button_pin));
  ButtonState_foot_button();
}
