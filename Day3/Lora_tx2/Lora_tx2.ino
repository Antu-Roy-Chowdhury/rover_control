#include <SPI.h>
#include <LoRa.h>

// Pin mapping (UNCHANGED)
#define SCK 18
#define MISO 19
#define MOSI 27
#define SS 5
#define RST 14
#define DIO0 26

String incoming = "";

void setup() {
  Serial.begin(115200);
  while (!Serial);

  Serial.println("LoRa TX Ready");

  // LoRa init
  SPI.begin(SCK, MISO, MOSI, SS);
  LoRa.setPins(SS, RST, DIO0);
  delay(500);

  if (!LoRa.begin(433E6)) {
    Serial.println("LoRa init failed!");
    while (1);
  }

  Serial.println("LoRa OK. Waiting Serial Commands...");
}

void loop() {

  // ======================================================
  //  Read full line from Serial sent by Python
  // ======================================================
  while (Serial.available()) {
    char c = Serial.read();

    if (c == '\n') {
      processCommand(incoming);
      incoming = "";
    } else {
      incoming += c;
    }
  }
}

void processCommand(String cmd) {

  cmd.trim();
  if (cmd.length() == 0) return;

  // Show locally
  Serial.print("→ TX: ");
  Serial.println(cmd);

  // ======================================================
  //          SEND EXACT COMMAND OVER LORA
  // ======================================================
  LoRa.beginPacket();
  LoRa.print(cmd);
  LoRa.endPacket();
}
