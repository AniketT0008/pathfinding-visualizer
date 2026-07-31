/*
 * Pathfinding Visualization Robot — ESP32-S3 + L298N firmware
 *
 * Hardware: ESP32-S3, L298N, 2x gearbox motors (diff drive)
 *
 * Default wiring (change if yours differs):
 *   IN1->10  IN2->11  IN3->12  IN4->13  ENA->14  ENB->21  GND->GND
 *   Motor supply on L298N 12V terminal — NOT the ESP 3.3V pin.
 *
 * Protocol (TCP :80, line ending \r or \n):
 *   FORWARD | BACKWARD | LEFT | RIGHT | STOP
 *   FORWARD:400   (ms, then auto-stop)
 *   LEFT:350 | RIGHT:350 | BACKWARD:400
 *   PING -> PONG
 *
 * Arduino IDE board: "ESP32S3 Dev Module"
 */

#include <WiFi.h>

const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

// ESP32-S3 friendly GPIOs (avoid USB 19/20 and strapping 0/3/45/46)
#define IN1 10
#define IN2 11
#define IN3 12
#define IN4 13
#define ENA 14
#define ENB 21

int LEFT_SPEED = 140;
int RIGHT_SPEED = 140;
int TURN_SPEED = 130;

WiFiServer server(80);

bool timedActive = false;
unsigned long timedEndMs = 0;

void stopMotors();
void moveForward();
void moveBackward();
void turnLeft();
void turnRight();
void applyCommand(String cmd, int durationMs);

void setup() {
  Serial.begin(115200);
  delay(200);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  stopMotors();

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(400);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Connected. ESP32-S3 IP: ");
  Serial.println(WiFi.localIP());
  Serial.println("Put this IP into robot_client.py -> ESP32_IP");

  server.begin();
}

void loop() {
  if (timedActive && millis() >= timedEndMs) {
    stopMotors();
    timedActive = false;
    Serial.println("Timed move done -> STOP");
  }

  WiFiClient client = server.available();
  if (!client) return;

  unsigned long startWait = millis();
  while (client.connected() && !client.available() && millis() - startWait < 500) {
    delay(1);
  }

  String request = client.readStringUntil('\n');
  request.trim();
  Serial.print("CMD: ");
  Serial.println(request);

  String reply = "OK";
  if (request.equalsIgnoreCase("PING")) {
    reply = "PONG";
  } else if (request.length() > 0) {
    int colon = request.indexOf(':');
    String cmd = request;
    int durationMs = -1;
    if (colon > 0) {
      cmd = request.substring(0, colon);
      durationMs = request.substring(colon + 1).toInt();
    }
    cmd.toUpperCase();
    applyCommand(cmd, durationMs);
  }

  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/plain");
  client.println("Connection: close");
  client.println();
  client.println(reply);
  client.stop();
}

void applyCommand(String cmd, int durationMs) {
  timedActive = false;

  if (cmd == "FORWARD") moveForward();
  else if (cmd == "BACKWARD") moveBackward();
  else if (cmd == "LEFT") turnLeft();
  else if (cmd == "RIGHT") turnRight();
  else if (cmd == "STOP") { stopMotors(); return; }
  else { Serial.println("Unknown command"); return; }

  if (durationMs > 0) {
    timedActive = true;
    timedEndMs = millis() + (unsigned long)durationMs;
  }
}

void moveForward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, LEFT_SPEED);
  analogWrite(ENB, RIGHT_SPEED);
}

void moveBackward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, LEFT_SPEED);
  analogWrite(ENB, RIGHT_SPEED);
}

void turnLeft() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, TURN_SPEED);
  analogWrite(ENB, TURN_SPEED);
}

void turnRight() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, TURN_SPEED);
  analogWrite(ENB, TURN_SPEED);
}

void stopMotors() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}
