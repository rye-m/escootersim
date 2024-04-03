
// // Arduino pin numbers
// const int X_pin = 0; // analog pin connected to X output

// void setup() {
//   Serial.begin(115200);
// }

// void loop() {
//   int deg = analogRead(X_pin);
//   Serial.println(deg);
//   // Serial.println(map(deg, 920, 1025, 55, -55));
//   // if (deg < 250) Serial.println(map(deg, 0, 250, -180, 0));
//   // else Serial.println(map(deg, 250, 500, 0, 180));
//   delay(50);
// }



// Arduino pin numbers
const int X_pin = 0; // analog pin connected to X output
const int Y_pin = 1; // analog pin connected to Y output

void setup() {
  Serial.begin(115200);
}

void loop() {
  // Serial.print(millis());
  // Serial.print(",");
  Serial.print(map(analogRead(X_pin), 1023, 0, -100, 100)/100.00);
  // Serial.print(analogRead(X_pin));
  Serial.print(",");
  Serial.println(map(analogRead(Y_pin), 0, 1023, -100, 100)/100.00);
  // Serial.println(analogRead(Y_pin));
  delay(9);
}