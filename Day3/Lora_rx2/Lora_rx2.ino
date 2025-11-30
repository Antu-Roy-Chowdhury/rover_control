#include <SPI.h>
#include <LoRa.h>

// SAME pin mapping as TX
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

  Serial.println("LoRa initialized & waiting for packets...");
}

void loop() {
  // Try to parse received packet
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    Serial.println("---- Packet Received ----");

    String received = "";
    while (LoRa.available()) {
      received += (char)LoRa.read();
    }

    Serial.print("Message: ");
    Serial.println(received);

    // RSSI signal strength
    Serial.print("RSSI: ");
    Serial.println(LoRa.packetRssi());

    Serial.println("-------------------------");
  }
}
