#include <DHT.h>

#define DHTPIN 14        // DHT11 connected to GPIO14
#define DHTTYPE DHT11

#define SOIL_PIN 34      // Soil moisture sensor (analog)
#define WATER_PIN 35     // Potentiometer simulating water purity
#define LED_PIN 12       // LED indicator

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
}

void loop() {
  // Read DHT11 values
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  // Read soil moisture and water purity
  int soil = analogRead(SOIL_PIN);
  int water = analogRead(WATER_PIN);

  // Display readings
  Serial.println("-------- Sensor Readings --------");
  Serial.print("Temperature: ");
  Serial.print(temp);
  Serial.println(" °C");

  Serial.print("Humidity: ");
  Serial.print(hum);
  Serial.println(" %");

  Serial.print("Soil Moisture (0-4095): ");
  Serial.println(soil);

  Serial.print("Water Purity (0-4095): ");
  Serial.println(water);

  // Alert thresholds
  bool soilDry = soil < 1500;         // adjust as needed
  bool waterDirty = water > 3000;     // adjust as needed

  // LED blinking logic
  if (soilDry && waterDirty) {
    Serial.println("⚠️ ALERT: Soil dry AND Water impure!");
    digitalWrite(LED_PIN, HIGH);
    delay(200);
    digitalWrite(LED_PIN, LOW);
    delay(200);
  }
  else if (soilDry) {
    Serial.println("⚠️ ALERT: Soil is dry!");
    digitalWrite(LED_PIN, HIGH);
    delay(600);
    digitalWrite(LED_PIN, LOW);
    delay(600);
  }
  else if (waterDirty) {
    Serial.println("⚠️ ALERT: Water is impure!");
    digitalWrite(LED_PIN, HIGH);
    delay(350);
    digitalWrite(LED_PIN, LOW);
    delay(350);
  }
  else {
    Serial.println("✅ All conditions normal.");
    digitalWrite(LED_PIN, LOW);
    delay(1000);
  }

  Serial.println("----------------------------------");
}
