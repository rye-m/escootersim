uint32_t  navi_throttle_LastTimerTick;

void Navi_ButtonState_throttle(){
  static int state = 0;
  uint32_t Ti;
  static uint32_t DoubleClickTick;
  
  switch(state){
    case 0:                                             // ボタン押下チェックstate
            if(isPressed(throttle_pin, throttle_th)){                   // プルアップされているので押下でL
              navi_throttle_LastTimerTick = millis();                 // 押下時の時間セット
              state = 1;
            }
            break;
    case 1:                                             // ボタン離しチェックstate
            if(! isPressed(throttle_pin, throttle_th)){                   // 立ち上がりを検出
              Ti = millis() - navi_throttle_LastTimerTick;
              if(Ti >= 500 ){                           // 500ms超えた？
                Serial.println("long press: none");          // 長押し確定
                // sendRequest("api",  "previous");
                state = 0;
              } else if(Ti >= 100){                     // シングルクリック仮確定
//              Serial.println("1:click!");
                DoubleClickTick =  millis();            // シングルクリック時の時間格納
                state = 2;
              }
            }
            break;
    case 2:                                             // ボタン押下チェックstate
          if(isPressed(throttle_pin, throttle_th)){                     // プルアップされているので押下でL
              navi_throttle_LastTimerTick = millis();                 // 押下時の時間セット
              state = 3;
            }
            if( millis()-DoubleClickTick >= 500){       // シングルクリック確定
                Serial.println("click: show/hide ETA");
                sendRequest("navi",  "ETA");
                state = 0;
            }
            break;
    case 3:                                             // ボタン離しチェックstate
            if(! isPressed(throttle_pin, throttle_th)){                   // 立ち上がりを検出
              Ti = millis() - navi_throttle_LastTimerTick;
              if(Ti >= 500 ){                           // 500ms超えた？
                Serial.println("long press: none");          // シングルクリック->長押し確定
                // sendRequest("api",  "previous");
                state = 0;
              } else if(Ti >= 250){
                Ti = millis()-DoubleClickTick;
//              Serial.println(Ti,DEC);
                if( Ti <= 700 and Ti > 300){                         // シングルクリックから500ms以内だったら、ダブルクリック確定
                  Serial.println("Doble click: zoom_in/out");
                  sendRequest("navi",  "zoom");
                  state = 0;
                } else {
                  Serial.println("click: show/hide ETA");
                  sendRequest("navi",  "ETA");
                  state = 0;                  
              }
            }
            break;
    default:
          break;
    }
  }            
}

void navi_throttle_setup(){
  sendRequest("api",  "navi_throttle_connected");
}

void navi_throttle_loop() {
  // Serial.println(analogRead(throttle_pin));
  Navi_ButtonState_throttle();
}
