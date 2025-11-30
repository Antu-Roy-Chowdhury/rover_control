#include <HardwareSerial.h>

// use UART2 on ESP32
HardwareSerial LoRaSerial(2);
LoraSerial.begin(9600,Serial_8IN, RX_PIN, TX_PIN);

void setup() {
  Serial.begin(115200);

  // RX = 16, TX = 17 (you can change if needed)
  LoRaSerial.begin(9600, SERIAL_8N1, 16, 17);

  Serial.println("ESP32 LoRa UART Ready");
}

void loop() {
  // send data to LoRa
  LoRaSerial.println("Hello");

  // read data from LoRa
  if (LoRaSerial.available()) {
    String data = LoRaSerial.readStringUntil('\n');
    Serial.print("Received: ");
    Serial.println(data);
  }

  delay(1000);
}
