#include <Adafruit_NeoPixel.h>

// How many internal neopixels do we have? some boards have more than one!
// #define NUMPIXELS        1
// #define NUMPIXELS        1

// Adafruit_NeoPixel neopixels(NUMPIXELS, PIN_NEOPIXEL, NEO_GRB + NEO_KHZ800);
uint32_t  LastTimerTick_foot;
const int input_pin = 23; // analog pin connected to X output


void ButtonState_foot_button(){
  static int state = 0;
  uint32_t Ti;
  static uint32_t DoubleClickTick;
  
  switch(state){
    case 0:                                             // ボタン押下チェックstate
            if(! digitalRead(input_pin)){                   // プルアップされているので押下でL
              LastTimerTick_foot = millis();                 // 押下時の時間セット
              state = 1;
            }
            break;
    case 1:                                             // ボタン離しチェックstate
            if(digitalRead(input_pin)){                   // 立ち上がりを検出
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
          if(! digitalRead(input_pin)){                     // プルアップされているので押下でL
              LastTimerTick_foot = millis();                 // 押下時の時間セット
              state = 3;
            }
            if( millis()-DoubleClickTick >= 500){       // シングルクリック確定
                Serial.println("click: play/puase");
                playOrPause();
                state = 0;
            }
            break;
    case 3:                                             // ボタン離しチェックstate
            if(digitalRead(input_pin)){                   // 立ち上がりを検出
              Ti = millis() - LastTimerTick_foot;
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

void spotify_foot_button_setup(){
  Serial.begin(112000);
  pinMode(input_pin, INPUT_PULLUP);  // set our pin to an input with a pullup resistor

  if (digitalRead(input_pin)) {
    Serial.println("Device acknowledged.");
  }
//   #if defined(NEOPIXEL_POWER)
//   // If this board has a power control pin, we must set it to output and high
//   // in order to enable the NeoPixels. We put this in an #if defined so it can
//   // be reused for other boards without compilation errors
//   pinMode(NEOPIXEL_POWER, OUTPUT);
//   digitalWrite(NEOPIXEL_POWER, HIGH);
// #endif

//   neopixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
//   neopixels.setBrightness(20); // not so bright

  sendRequest("api",  "spotify_button_connected");
}


void spotify_foot_button_loop() {
  // Serial.println(digitalRead(input_pin));
  ButtonState_foot_button();
}
