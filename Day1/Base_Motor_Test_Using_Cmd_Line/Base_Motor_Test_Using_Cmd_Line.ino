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

// ===== PWM Config =====
#define PWM_FREQ 5000
#define PWM_RES 8  // 8-bit (0–255)

// ===== PWM Channels =====
#define CH_L1_FWD 0
#define CH_L1_BWD 1
#define CH_L2_FWD 2
#define CH_L2_BWD 3
#define CH_R1_FWD 4
#define CH_R1_BWD 5
#define CH_R2_FWD 6
#define CH_R2_BWD 7

int motorSpeed = 150; // Default speed (0–255)
String command = "";  // Buffer for serial input

// ====== Setup ======
void setup() {
  Serial.begin(115200);
  Serial.println("ESP32 Motor Control Ready!");
  Serial.println("Commands: forward, backward, left, right, stop, speed <0-255>");

  // Left motors
  ledcSetup(CH_L1_FWD, PWM_FREQ, PWM_RES); ledcAttachPin(L1_FWD, CH_L1_FWD);
  ledcSetup(CH_L1_BWD, PWM_FREQ, PWM_RES); ledcAttachPin(L1_BWD, CH_L1_BWD);
  ledcSetup(CH_L2_FWD, PWM_FREQ, PWM_RES); ledcAttachPin(L2_FWD, CH_L2_FWD);
  ledcSetup(CH_L2_BWD, PWM_FREQ, PWM_RES); ledcAttachPin(L2_BWD, CH_L2_BWD);

  // Right motors
  ledcSetup(CH_R1_FWD, PWM_FREQ, PWM_RES); ledcAttachPin(R1_FWD, CH_R1_FWD);
  ledcSetup(CH_R1_BWD, PWM_FREQ, PWM_RES); ledcAttachPin(R1_BWD, CH_R1_BWD);
  ledcSetup(CH_R2_FWD, PWM_FREQ, PWM_RES); ledcAttachPin(R2_FWD, CH_R2_FWD);
  ledcSetup(CH_R2_BWD, PWM_FREQ, PWM_RES); ledcAttachPin(R2_BWD, CH_R2_BWD);

  stopMotors();
}

// ====== Helper Functions ======
void stopMotors() {
  for (int ch = 0; ch <= 7; ch++) {
    ledcWrite(ch, 0);
  }
}

void moveForward(int speed) {
  ledcWrite(CH_L1_FWD, speed); ledcWrite(CH_L1_BWD, 0);
  ledcWrite(CH_L2_FWD, speed); ledcWrite(CH_L2_BWD, 0);
  ledcWrite(CH_R1_FWD, speed); ledcWrite(CH_R1_BWD, 0);
  ledcWrite(CH_R2_FWD, speed); ledcWrite(CH_R2_BWD, 0);
}

void moveBackward(int speed) {
  ledcWrite(CH_L1_FWD, 0); ledcWrite(CH_L1_BWD, speed);
  ledcWrite(CH_L2_FWD, 0); ledcWrite(CH_L2_BWD, speed);
  ledcWrite(CH_R1_FWD, 0); ledcWrite(CH_R1_BWD, speed);
  ledcWrite(CH_R2_FWD, 0); ledcWrite(CH_R2_BWD, speed);
}

void turnLeft(int speed) {
  ledcWrite(CH_L1_FWD, 0); ledcWrite(CH_L1_BWD, speed);
  ledcWrite(CH_L2_FWD, 0); ledcWrite(CH_L2_BWD, speed);
  ledcWrite(CH_R1_FWD, speed); ledcWrite(CH_R1_BWD, 0);
  ledcWrite(CH_R2_FWD, speed); ledcWrite(CH_R2_BWD, 0);
}

void turnRight(int speed) {
  ledcWrite(CH_L1_FWD, speed); ledcWrite(CH_L1_BWD, 0);
  ledcWrite(CH_L2_FWD, speed); ledcWrite(CH_L2_BWD, 0);
  ledcWrite(CH_R1_FWD, 0); ledcWrite(CH_R1_BWD, speed);
  ledcWrite(CH_R2_FWD, 0); ledcWrite(CH_R2_BWD, speed);
}

// ====== Command Parser ======
void handleCommand(String cmd) {
  cmd.trim();
  cmd.toLowerCase();

  if (cmd == "forward") {
    moveForward(motorSpeed);
    Serial.println("Moving forward");
  } 
  else if (cmd == "backward") {
    moveBackward(motorSpeed);
    Serial.println("Moving backward");
  } 
  else if (cmd == "left") {
    turnLeft(motorSpeed);
    Serial.println("Turning left");
  } 
  else if (cmd == "right") {
    turnRight(motorSpeed);
    Serial.println("Turning right");
  } 
  else if (cmd == "stop") {
    stopMotors();
    Serial.println("Motors stopped");
  } 
  else if (cmd.startsWith("speed ")) {
    int val = cmd.substring(6).toInt();
    if (val >= 0 && val <= 255) {
      motorSpeed = val;
      Serial.print("Speed set to ");
      Serial.println(motorSpeed);
    } else {
      Serial.println("Invalid speed! Enter 0–255");
    }
  } 
  else {
    Serial.println("Unknown command!");
  }
}

// ====== Main Loop ======
void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      if (command.length() > 0) {
        handleCommand(command);
        command = "";
      }
    } else {
      command += c;
    }
  }
}
