#include <Arduino.h>
#include <stdio.h>
// #include "pico/stdlib.h"
// #include "hardware/adc.h"

// put function declarations here:
int myFunction(int, int);

const int A_pin = 0; // analog pin connected to X output
const int B_pin = 1; // analog pin connected to Y output
const int S_pin = 2; // analog pin connected to Y output

void setup() {
  Serial.begin(115200);
}

void loop() {
  Serial.print(map(analogRead(A_pin), 260, 820, 0, 100)/100.00);
  Serial.print(",");
  Serial.print(map(analogRead(B_pin), 290, 690, 0, 100)/100.00);
  Serial.print(",");
  Serial.println(0);
  delay(9);
}

// put function definitions here:
int myFunction(int x, int y) {
  return x + y;
}