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
  int packetSize = LoRa.parsePacket();
  if (packetSize) {

    String received = "";
    while (LoRa.available()) {
      received += (char)LoRa.read();
    }

    received.trim();  // remove \n or spaces

    Serial.println("---- Packet Received ----");
    Serial.print("Raw: ");
    Serial.println(received);

    // ---------------------------
    // SPLIT INTO DIRECTION & SPEED
    // ---------------------------
    String direction = "";
    int speed = 0;

    int sepIndex = received.indexOf(':');

    if (sepIndex != -1) {
      direction = received.substring(0, sepIndex);
      String spdStr = received.substring(sepIndex + 1);
      speed = spdStr.toInt();
    } else {
      direction = received;  // if speed not included
    }

    // Print extracted values
    Serial.print("Direction: ");
    Serial.println(direction);

    Serial.print("Speed: ");
    Serial.println(speed);

    Serial.print("RSSI: ");
    Serial.println(LoRa.packetRssi());
    Serial.println("-------------------------");
  }
}