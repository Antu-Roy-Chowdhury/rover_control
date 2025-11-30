#include <ESP32Servo.h>  // Correct library for ESP32

// ===== LEFT SIDE MOTORS (BTS7960 #1) =====
#define L1_FWD 16
#define L1_BWD 17
#define L2_FWD 18
#define L2_BWD 19

// ===== RIGHT SIDE MOTORS (BTS7960 #2) =====
#define R1_FWD 14
#define R1_BWD 12
#define R2_FWD 27
#define R2_BWD 26

// ===== SERVO PINS =====
#define SERVO1_PIN 32

#define SERVO2_PIN 33

Servo servo1;
Servo servo2;

// ===== PWM Config =====
#define PWM_FREQ 5000
#define PWM_RES 8  // 8-bit (0–255)

// ✅ Use higher channels for motors (avoid servo interference)
#define CH_L1_FWD 8
#define CH_L1_BWD 9
#define CH_L2_FWD 10
#define CH_L2_BWD 11
#define CH_R1_FWD 12
#define CH_R1_BWD 13
#define CH_R2_FWD 14
#define CH_R2_BWD 15

// ===== Setup =====
void setup() {
  Serial.begin(115200);
  Serial.println("ESP32 Motor & Servo Controller Ready!");

  // === Setup PWM for Left Motors ===
  ledcSetup(CH_L1_FWD, PWM_FREQ, PWM_RES);
  ledcAttachPin(L1_FWD, CH_L1_FWD);
  ledcSetup(CH_L1_BWD, PWM_FREQ, PWM_RES);
  ledcAttachPin(L1_BWD, CH_L1_BWD);

  ledcSetup(CH_L2_FWD, PWM_FREQ, PWM_RES);
  ledcAttachPin(L2_FWD, CH_L2_FWD);
  ledcSetup(CH_L2_BWD, PWM_FREQ, PWM_RES);
  ledcAttachPin(L2_BWD, CH_L2_BWD);

  // === Setup PWM for Right Motors ===
  ledcSetup(CH_R1_FWD, PWM_FREQ, PWM_RES);
  ledcAttachPin(R1_FWD, CH_R1_FWD);
  ledcSetup(CH_R1_BWD, PWM_FREQ, PWM_RES);
  ledcAttachPin(R1_BWD, CH_R1_BWD);

  ledcSetup(CH_R2_FWD, PWM_FREQ, PWM_RES);
  ledcAttachPin(R2_FWD, CH_R2_FWD);
  ledcSetup(CH_R2_BWD, PWM_FREQ, PWM_RES);
  ledcAttachPin(R2_BWD, CH_R2_BWD);

  // === Servo setup ===
  servo1.setPeriodHertz(50);   // Standard 50Hz servo frequency
  servo2.setPeriodHertz(50);
  servo1.attach(SERVO1_PIN, 500, 2400);  // Min/max pulse widths (µs)
  servo2.attach(SERVO2_PIN, 500, 2400);
  servo1.write(90); // Neutral
  servo2.write(90);
}

// ===== Motor Control Functions =====
void stopMotors() {
  for (int ch = 8; ch <= 15; ch++) {
    ledcWrite(ch, 0);
  }
}

void moveForward(int speed) {
  ledcWrite(CH_L1_FWD, speed);
  ledcWrite(CH_L1_BWD, 0);
  ledcWrite(CH_L2_FWD, speed);
  ledcWrite(CH_L2_BWD, 0);
  ledcWrite(CH_R1_FWD, speed);
  ledcWrite(CH_R1_BWD, 0);
  ledcWrite(CH_R2_FWD, speed);
  ledcWrite(CH_R2_BWD, 0);
}

void moveBackward(int speed) {
  ledcWrite(CH_L1_FWD, 0);
  ledcWrite(CH_L1_BWD, speed);
  ledcWrite(CH_L2_FWD, 0);
  ledcWrite(CH_L2_BWD, speed);
  ledcWrite(CH_R1_FWD, 0);
  ledcWrite(CH_R1_BWD, speed);
  ledcWrite(CH_R2_FWD, 0);
  ledcWrite(CH_R2_BWD, speed);
}

void turnLeft(int speed) {
  ledcWrite(CH_L1_FWD, 0);
  ledcWrite(CH_L1_BWD, speed);
  ledcWrite(CH_L2_FWD, 0);
  ledcWrite(CH_L2_BWD, speed);
  ledcWrite(CH_R1_FWD, speed);
  ledcWrite(CH_R1_BWD, 0);
  ledcWrite(CH_R2_FWD, speed);
  ledcWrite(CH_R2_BWD, 0);
}

void turnRight(int speed) {
  ledcWrite(CH_L1_FWD, speed);
  ledcWrite(CH_L1_BWD, 0);
  ledcWrite(CH_L2_FWD, speed);
  ledcWrite(CH_L2_BWD, 0);
  ledcWrite(CH_R1_FWD, 0);
  ledcWrite(CH_R1_BWD, speed);
  ledcWrite(CH_R2_FWD, 0);
  ledcWrite(CH_R2_BWD, speed);
}

// ===== Main Loop =====
void loop() {
  static int speed = 150;
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    // ===== Motor Commands =====
    if (cmd.equalsIgnoreCase("forward")) {
      Serial.println("Moving Forward");
      moveForward(speed);
    } 
    else if (cmd.equalsIgnoreCase("backward")) {
      Serial.println("Moving Backward");
      moveBackward(speed);
    } 
    else if (cmd.equalsIgnoreCase("left")) {
      Serial.println("Turning Left");
      turnLeft(speed);
    } 
    else if (cmd.equalsIgnoreCase("right")) {
      Serial.println("Turning Right");
      turnRight(speed);
    } 
    else if (cmd.equalsIgnoreCase("stop")) {
      Serial.println("Motors Stopped");
      stopMotors();
    }

    // ===== Servo Control =====
    else if (cmd.startsWith("servo1")) {
      int angle = cmd.substring(6).toInt();
      angle = constrain(angle, 0, 180);
      servo1.write(angle);
      Serial.printf("Servo1 set to %d°\n", angle);
    } 
    else if (cmd.startsWith("servo2")) {
      int angle = cmd.substring(6).toInt();
      angle = constrain(angle, 0, 180);
      servo2.write(angle);
      Serial.printf("Servo2 set to %d°\n", angle);
    } 

    // ===== Speed Adjust =====
    else if (cmd.startsWith("speed")) {
      speed = cmd.substring(5).toInt();
      speed = constrain(speed, 0, 255);
      Serial.printf("Speed set to %d\n", speed);
    } 
    else {
      Serial.println("Unknown command!");
    }
  }
}
