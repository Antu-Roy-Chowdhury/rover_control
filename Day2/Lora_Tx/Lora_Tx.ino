#include <SPI.h>
#include <LoRa.h>

// Pin mapping
#define SCK 18
#define MISO 19
#define MOSI 27
#define SS 5
#define RST 14
#define DIO0 26

int counter = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial);
  Serial.println("LoRa Transmitter (RA-02)");

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
  Serial.print("Sending packet: ");
  Serial.println(counter);

  // Begin packet
  LoRa.beginPacket();
  LoRa.print("Hello from ESP32 ");
  LoRa.print(counter);
  LoRa.endPacket(); // Transmit

  counter++;
  delay(2000); // Wait 2 seconds before next packet
}
