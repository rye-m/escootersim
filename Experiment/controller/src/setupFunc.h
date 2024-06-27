#include <WiFi.h>
#include <Wire.h>
    

void init_wifi() {
Serial.begin(115200);
delay(1000);

WiFi.mode(WIFI_STA); //Optional
WiFi.begin(ssid, password);
Serial.println("\nConnecting to Wi-Fi");

while(WiFi.status() != WL_CONNECTED){
    Serial.print(".");
    delay(100);
}

Serial.println("\nConnected to the WiFi network");
Serial.print("Local TinyPICO IP: ");
Serial.println(WiFi.localIP());

delay(1000);

}