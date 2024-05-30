uint32_t  LastTimerTick;

void ButtonState_button(){
  static int state = 0;
  uint32_t Ti;
  static uint32_t DoubleClickTick;
  
  switch(state){
    case 0:                                             // ボタン押下チェックstate
            if(button.isPressed()){                   // プルアップされているので押下でL
              LastTimerTick = millis();                 // 押下時の時間セット
              state = 1;
              button.LEDon(100);
            }
            break;
    case 1:                                             // ボタン離しチェックstate
            if(! button.isPressed()){                   // 立ち上がりを検出
              Ti = millis() - LastTimerTick;
              button.LEDoff();
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
          if(button.isPressed()){                     // プルアップされているので押下でL
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
            if(! button.isPressed()){                   // 立ち上がりを検出
              Ti = millis() - LastTimerTick;
              button.LEDoff();
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
                  Serial.println("click: play/puase");           // 
                  playOrPause();
                  state = 0;                  
              }
            }
            break;
    default:
          break;
    }

  }            
}

void spotify_button_setup(){
    
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

  sendRequest("api",  "spotify_button_connected");
}


void spotify_button_loop() {
  ButtonState_button();
  }