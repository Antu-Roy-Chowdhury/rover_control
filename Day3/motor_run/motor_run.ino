// ==================== MOTOR ESP32 - FULL FINAL CODE ====================
// Perfect for Python bridge over USB (ttyUSB1) + works with Serial Monitor
// ======================================================================

// ===== MOTOR PINS =====
#define L1_FWD 16
#define L1_BWD 17
#define L2_FWD 18
#define L2_BWD 19
#define R1_FWD 14
#define R1_BWD 12
#define R2_FWD 27
#define R2_BWD 26

// ===== PWM CONFIG =====
#define PWM_FREQ 5000
#define PWM_RES  8

// ===== PWM CHANNELS =====
#define CH_L1_FWD 0
#define CH_L1_BWD 1
#define CH_L2_FWD 2
#define CH_L2_BWD 3
#define CH_R1_FWD 4
#define CH_R1_BWD 5
#define CH_R2_FWD 6
#define CH_R2_BWD 7

int motorSpeed = 150;  // default speed if not specified

// ======================================================================
void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("\n\n=== MOTOR ESP32 READY (Bridge Mode) ===");
  Serial.println("Send commands like: f:180  lf:90  stop  rb:120");

  // Setup all PWM channels
  ledcSetup(CH_L1_FWD, PWM_FREQ, PWM_RES); ledcAttachPin(L1_FWD, CH_L1_FWD);
  ledcSetup(CH_L1_BWD, PWM_FREQ, PWM_RES); ledcAttachPin(L1_BWD, CH_L1_BWD);
  ledcSetup(CH_L2_FWD, PWM_FREQ, PWM_RES); ledcAttachPin(L2_FWD, CH_L2_FWD);
  ledcSetup(CH_L2_BWD, PWM_FREQ, PWM_RES); ledcAttachPin(L2_BWD, CH_L2_BWD);
  ledcSetup(CH_R1_FWD, PWM_FREQ, PWM_RES); ledcAttachPin(R1_FWD, CH_R1_FWD);
  ledcSetup(CH_R1_BWD, PWM_FREQ, PWM_RES); ledcAttachPin(R1_BWD, CH_R1_BWD);
  ledcSetup(CH_R2_FWD, PWM_FREQ, PWM_RES); ledcAttachPin(R2_FWD, CH_R2_FWD);
  ledcSetup(CH_R2_BWD, PWM_FREQ, PWM_RES); ledcAttachPin(R2_BWD, CH_R2_BWD);

  stopMotors();
}

// ======================================================================
void loop() {
  // Listen for commands from Python bridge OR Serial Monitor
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    if (input.length() > 0) {
      handleCommand(input);
    }
  }
}

// ======================================================================
void handleCommand(String input) {
  input.trim();
  input.toLowerCase();

  // Allow both "lf:80" and just "lf" (uses last speed)
  String dir;
  int spd = motorSpeed;  // default = last used speed

  if (input.indexOf(':') != -1) {
    dir = input.substring(0, input.indexOf(':'));
    spd = input.substring(input.indexOf(':') + 1).toInt();
    if (spd < 0 || spd > 255) spd = motorSpeed;
  } else {
    dir = input;
  }

  motorSpeed = spd;  // remember for next time

  // ------------ BASIC DIRECTIONS -------------
  if (dir == "f" || dir == "forward") {
    moveForward(spd);
    Serial.printf("FORWARD @ %d\n", spd);
  }
  else if (dir == "b" || dir == "backward") {
    moveBackward(spd);
    Serial.printf("BACKWARD @ %d\n", spd);
  }
  else if (dir == "l" || dir == "left") {
    turnLeft(spd);
    Serial.printf("LEFT @ %d\n", spd);
  }
  else if (dir == "r" || dir == "right") {
    turnRight(spd);
    Serial.printf("RIGHT @ %d\n", spd);
  }

  // ------------ DIAGONALS -------------
  else if (dir == "lf") {
    moveDiagonalLeftForward(spd);
    Serial.printf("LEFT-FORWARD @ %d\n", spd);
  }
  else if (dir == "rf") {
    moveDiagonalRightForward(spd);
    Serial.printf("RIGHT-FORWARD @ %d\n", spd);
  }
  else if (dir == "lb") {
    moveDiagonalLeftBackward(spd);
    Serial.printf("LEFT-BACKWARD @ %d\n", spd);
  }
  else if (dir == "rb") {
    moveDiagonalRightBackward(spd);
    Serial.printf("RIGHT-BACKWARD @ %d\n", spd);
  }

  // ------------ STOP -------------
  else if (dir == "stop" || dir == "s") {
    stopMotors();
    Serial.println("STOP");
  }

  else {
    Serial.println("Unknown command: " + dir);
  }
}

// ======================================================================
// Motor control functions
// ======================================================================
void stopMotors() {
  for (int ch = 0; ch <= 7; ch++) ledcWrite(ch, 0);
}

void moveForward(int spd) {
  ledcWrite(CH_L1_FWD, spd); ledcWrite(CH_L1_BWD, 0);
  ledcWrite(CH_L2_FWD, spd); ledcWrite(CH_L2_BWD, 0);
  ledcWrite(CH_R1_FWD, spd); ledcWrite(CH_R1_BWD, 0);
  ledcWrite(CH_R2_FWD, spd); ledcWrite(CH_R2_BWD, 0);
}

void moveBackward(int spd) {
  ledcWrite(CH_L1_FWD, 0); ledcWrite(CH_L1_BWD, spd);
  ledcWrite(CH_L2_FWD, 0); ledcWrite(CH_L2_BWD, spd);
  ledcWrite(CH_R1_FWD, 0); ledcWrite(CH_R1_BWD, spd);
  ledcWrite(CH_R2_FWD, 0); ledcWrite(CH_R2_BWD, spd);
}

void turnLeft(int spd) {
  ledcWrite(CH_L1_FWD, 0); ledcWrite(CH_L1_BWD, spd);
  ledcWrite(CH_L2_FWD, 0); ledcWrite(CH_L2_BWD, spd);
  ledcWrite(CH_R1_FWD, spd); ledcWrite(CH_R1_BWD, 0);
  ledcWrite(CH_R2_FWD, spd); ledcWrite(CH_R2_BWD, 0);
}

void turnRight(int spd) {
  ledcWrite(CH_L1_FWD, spd); ledcWrite(CH_L1_BWD, 0);
  ledcWrite(CH_L2_FWD, spd); ledcWrite(CH_L2_BWD, 0);
  ledcWrite(CH_R1_FWD, 0); ledcWrite(CH_R1_BWD, spd);
  ledcWrite(CH_R2_FWD, 0); ledcWrite(CH_R2_BWD, spd);
}

void moveDiagonalLeftForward(int spd) {
  ledcWrite(CH_L1_FWD, spd/2); ledcWrite(CH_L1_BWD, 0);
  ledcWrite(CH_L2_FWD, spd/2); ledcWrite(CH_L2_BWD, 0);
  ledcWrite(CH_R1_FWD, spd);   ledcWrite(CH_R1_BWD, 0);
  ledcWrite(CH_R2_FWD, spd);   ledcWrite(CH_R2_BWD, 0);
}

void moveDiagonalRightForward(int spd) {
  ledcWrite(CH_L1_FWD, spd);   ledcWrite(CH_L1_BWD, 0);
  ledcWrite(CH_L2_FWD, spd);   ledcWrite(CH_L2_BWD, 0);
  ledcWrite(CH_R1_FWD, spd/2); ledcWrite(CH_R1_BWD, 0);
  ledcWrite(CH_R2_FWD, spd/2); ledcWrite(CH_R2_BWD, 0);
}

void moveDiagonalLeftBackward(int spd) {
  ledcWrite(CH_L1_FWD, 0); ledcWrite(CH_L1_BWD, spd/2);
  ledcWrite(CH_L2_FWD, 0); ledcWrite(CH_L2_BWD, spd/2);
  ledcWrite(CH_R1_FWD, 0); ledcWrite(CH_R1_BWD, spd);
  ledcWrite(CH_R2_FWD, 0); ledcWrite(CH_R2_BWD, spd);
}

void moveDiagonalRightBackward(int spd) {
  ledcWrite(CH_L1_FWD, 0); ledcWrite(CH_L1_BWD, spd);
  ledcWrite(CH_L2_FWD, 0); ledcWrite(CH_L2_BWD, spd);
  ledcWrite(CH_R1_FWD, 0); ledcWrite(CH_R1_BWD, spd/2);
  ledcWrite(CH_R2_FWD, 0); ledcWrite(CH_R2_BWD, spd/2);
}