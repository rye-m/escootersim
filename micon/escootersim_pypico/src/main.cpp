#include <Arduino.h>
#include <stdio.h>

const int A_pin = 0; // analog pin connected to X output
const int B_pin = 1; // analog pin connected to Y output
const int S_pin = 2; // analog pin connected to Z output

void setup() {
  Serial.begin(115200);
}

void loop() {

  Serial.print(map(analogRead(A_pin), 270, 800, 0, 100)/100.00);
  Serial.print(",");
  Serial.print(map(analogRead(B_pin), 295, 700, 0, 100)/100.00);
  Serial.print(",");
  Serial.println(map(analogRead(S_pin), 410, 813, 50, -45)/100.00); // C: 622
  delay(9);
}