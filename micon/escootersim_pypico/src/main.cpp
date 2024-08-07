#include <Arduino.h>
#include <stdio.h>
#include <Wire.h>
#include <Adafruit_LSM6DS3TRC.h>

const int A_pin = 0; // analog pin connected to X output
const int B_pin = 1; // analog pin connected to Y output
const int S_pin = 2; // analog pin connected to Z output

Adafruit_LSM6DS3TRC lsm6ds3trc;

void setup()
{
  Wire.begin();
  Serial.begin(115200);
  if (!lsm6ds3trc.begin_I2C(0x6A, &Wire))
  {
    while (1)
    {
      Serial.println("Failed to find LSM6DS3TR-C chip, check wiring.");
      delay(10);
    }
  }
  lsm6ds3trc.setAccelRange(LSM6DS_ACCEL_RANGE_2_G);
  lsm6ds3trc.setGyroRange(LSM6DS_GYRO_RANGE_250_DPS);
  lsm6ds3trc.setAccelDataRate(LSM6DS_RATE_104_HZ);
  lsm6ds3trc.setGyroDataRate(LSM6DS_RATE_104_HZ);
}

void loop()
{
  // Get a new normalized sensor event
  sensors_event_t accel;
  sensors_event_t gyro;
  sensors_event_t temp;
  lsm6ds3trc.getEvent(&accel, &gyro, &temp);

  Serial.print(map(analogRead(A_pin), 270, 800, 0, 100) / 100.00);
  Serial.print(",");
  Serial.print(map(analogRead(B_pin), 295, 700, 0, 100) / 100.00);
  Serial.print(",");
  Serial.print(map(analogRead(S_pin), 410, 813, 50, -45) / 100.00); // C: 622
  Serial.print(",");

  Serial.print(accel.acceleration.x);
  Serial.print(",");
  Serial.print(accel.acceleration.y);
  Serial.print(",");
  Serial.print(accel.acceleration.z);
  Serial.print(",");

  Serial.print(gyro.gyro.x);
  Serial.print(",");
  Serial.print(gyro.gyro.y);
  Serial.print(",");
  Serial.print(gyro.gyro.z);
  Serial.println();
  delay(9);
}