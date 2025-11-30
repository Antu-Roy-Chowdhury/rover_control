#include <SPI.h>
#include <LoRa.h>

// Pin mapping
#define SCK 18
#define MISO 19
#define MOSI 27
#define SS 5
#define RST 14
#define DIO0 26

void setup() {
  Serial.begin(115200);
  while (!Serial);
  Serial.println("LoRa Receiver (RA-02)");

  SPI.begin(SCK, MISO, MOSI, SS);
  LoRa.setPins(SS, RST, DIO0);
  delay(1000);

  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }

  Serial.println("LoRa initialized successfully!");
}

void loop() {
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    Serial.print("Received packet: ");

    while (LoRa.available()) {
      Serial.print((char)LoRa.read());
    }

    Serial.print("  |  RSSI: ");
    Serial.println(LoRa.packetRssi());
  }
}
