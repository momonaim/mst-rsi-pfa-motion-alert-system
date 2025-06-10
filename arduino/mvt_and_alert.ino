#include <Bridge.h>
#include <HttpClient.h>

const int pirPin = 2;      // PIR motion sensor
const int ledPin = 13;     // Status LED
const int buzzerPin = 8;   // Buzzer (optional)

bool motionActive = false; // Track if motion is happening
bool alertSent = false;    // Prevent duplicate alerts
unsigned long lastAlertTime = 0;  // Track last alert time
const unsigned long POST_ALERT_DELAY = 10000;  // 10-sec cooldown after alert

void setup() {
  pinMode(pirPin, INPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

  Bridge.begin();  
  Serial.begin(9600);
  while (!Serial);  // Wait for Serial Monitor (Yún)

  Serial.println("Motion Alert System Ready");
}

void loop() {
  // Check for motion
  if (digitalRead(pirPin) == HIGH) {
    digitalWrite(ledPin, HIGH);     // Visual indicator
    digitalWrite(buzzerPin, HIGH);  // Audible alert
    
    if (!alertSent && (millis() - lastAlertTime > POST_ALERT_DELAY)) {
      Serial.println("ALERT: Motion detected!");
      sendAlert();      // Blocks until HTTP completes
      alertSent = true; // Prevent duplicate alerts
      lastAlertTime = millis();  // Record alert time
    }
    motionActive = true;
  } 
  else {
    // No motion detected
    digitalWrite(ledPin, LOW);
    digitalWrite(buzzerPin, LOW);
    
    if (motionActive) {
      Serial.println("Motion stopped.");
      alertSent = false;  // Reset for next motion event
    }
    motionActive = false;
  }

  delay(200);  // Small delay for stability
}

// Sends HTTP request and waits for response (blocking)
void sendAlert() {
  playMelody();
  Serial.println("Sending HTTP alert...");
  
  HttpClient client;
  String url = "http://192.168.217.16:5000/alert";
  client.get(url);  // Send GET request

  // Wait for response (5s timeout)
  unsigned long startTime = millis();
  while (!client.available() && millis() - startTime < 5000) {
    delay(100);
  }

  // Print response (or timeout)
  if (client.available()) {
    Serial.println("Server Response:");
    while (client.available()) {
      Serial.print((char)client.read());
    }
    Serial.println();
  } 
  else {
    Serial.println("ERROR: No response (timeout)");
  }

  // Add extra delay after sending
  delay(2000);  
}

//Play Melody
void playMelody() {
  int notes[] = { 880, 660, 880, 660, 880 }; // A5 - E5 repeated
  int duration = 200;

  for (int i = 0; i < 5; i++) {
    tone(buzzerPin, notes[i], duration);
    delay(duration + 50);  // small pause between notes
  }

  noTone(buzzerPin);  // Stop any remaining sound
}