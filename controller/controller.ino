#include <SoftwareSerial.h>

SoftwareSerial lora(2, 3); // RX, TX

void setup() {
  Serial.begin(9600);
  lora.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    lora.print(c);
  }
}
