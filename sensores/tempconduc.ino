#include <OneWire.h>
#include <DallasTemperature.h>

// --- Pines para EC y Temperatura ---
#define EC_PIN A0
#define ONE_WIRE_BUS 2

// --- Pines para nivel de agua ---
#define TRIG_PIN 9
#define ECHO_PIN 10

// --- Pin para sensor de pH ---
#define PH_PIN A1

// --- Pines para módulo relay ---
#define RELAY_PERISTALTICA_1 3  // IN1 D3 bajar pH
#define RELAY_PERISTALTICA_2 4  // IN2 D4 subir pH
#define RELAY_PERISTALTICA_3 6  // IN5 D6 agregar nutrientes (tomates cherry)

// --- Configuración sensores ---
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// --- Parámetros EC ---
#define VREF 5.0
#define ADC_RESOLUTION 1024.0
float calibrationConstant = 1.0;

// --- Parámetros Nivel Agua ---
#define ALTURA_SENSOR_CM 30.0
#define OFFSET_CALIBRACION_CM 1.5
#define NIVEL_MINIMO_CM 5.0

// --- Rangos ideales ---
float idealPHMin = 5.5;
float idealPHMax = 7.5;
float idealECMin = 1.2;  // Ideal para tomates cherry: 1.2–2.5 mS/cm
float idealECMax = 2.5;

void setup() {
  Serial.begin(9600);
  sensors.begin();

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(RELAY_PERISTALTICA_1, OUTPUT);
  pinMode(RELAY_PERISTALTICA_2, OUTPUT);
  pinMode(RELAY_PERISTALTICA_3, OUTPUT);

  digitalWrite(RELAY_PERISTALTICA_1, HIGH);
  digitalWrite(RELAY_PERISTALTICA_2, HIGH);
  digitalWrite(RELAY_PERISTALTICA_3, HIGH);

  Serial.println("🔧 Iniciando sensores...");
  delay(1000);
}

float medirDistancia() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duracion = pulseIn(ECHO_PIN, HIGH, 30000);
  if (duracion == 0) return -1;

  float distancia = duracion * 0.034 / 2;
  distancia += OFFSET_CALIBRACION_CM;
  return distancia;
}

void loop() {
  float distancia = medirDistancia();
  float nivelAgua = ALTURA_SENSOR_CM - distancia;

  bool alertaNivel = false;
  if (distancia < 0 || nivelAgua < NIVEL_MINIMO_CM) {
    alertaNivel = true;
    nivelAgua = max(nivelAgua, 0);
  }

  sensors.requestTemperatures();
  float temperatura = sensors.getTempCByIndex(0);

  int analogValueEC = analogRead(EC_PIN);
  float voltageEC = (analogValueEC / ADC_RESOLUTION) * VREF;
  float ecValue = (voltageEC / calibrationConstant) * (1.0 + 0.0185 * (temperatura - 25.0));

  int rawPH = analogRead(PH_PIN);
  float voltagePH = rawPH * (5.0 / 1023.0);
  float phValue = -6.475 * voltagePH + 25.99;

  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "TEST") {
      Serial.println("OK");
    } else if (cmd == "READ_SENSORS") {
      Serial.print("{");
      Serial.print("\"nivelAgua_cm\":"); Serial.print(nivelAgua, 2); Serial.print(",");
      Serial.print("\"temp_C\":"); Serial.print(temperatura, 2); Serial.print(",");
      Serial.print("\"EC_mS_cm\":"); Serial.print(ecValue, 2); Serial.print(",");
      Serial.print("\"pH\":"); Serial.print(phValue, 2); Serial.print(",");
      Serial.print("\"alertaNivel\":"); Serial.print(alertaNivel ? 1 : 0);
      Serial.println("}");
    } else if (cmd.startsWith("ACTIVATE_PUMP")) {
      int pumpNumber = cmd.substring(14).toInt();
      if (pumpNumber == 1) digitalWrite(RELAY_PERISTALTICA_1, LOW);
      if (pumpNumber == 2) digitalWrite(RELAY_PERISTALTICA_2, LOW);
      if (pumpNumber == 3) digitalWrite(RELAY_PERISTALTICA_3, LOW);
    } else if (cmd.startsWith("DEACTIVATE_PUMP")) {
      int pumpNumber = cmd.substring(17).toInt();
      if (pumpNumber == 1) digitalWrite(RELAY_PERISTALTICA_1, HIGH);
      if (pumpNumber == 2) digitalWrite(RELAY_PERISTALTICA_2, HIGH);
      if (pumpNumber == 3) digitalWrite(RELAY_PERISTALTICA_3, HIGH);
    }
  }

  Serial.print("nivelAgua_cm:");
  Serial.print(nivelAgua, 2);
  Serial.print(",temp_C:");
  Serial.print(temperatura, 2);
  Serial.print(",EC_mS_cm:");
  Serial.print(ecValue, 2);
  Serial.print(",pH:");
  Serial.print(phValue, 2);
  Serial.print(",alertaNivel:");
  Serial.println(alertaNivel ? "1" : "0");

  // --- Control automático de bombas ---
  // pH bajo: subir pH
  if (phValue < 6.0) digitalWrite(RELAY_PERISTALTICA_2, LOW);
  else if (phValue > idealPHMax) digitalWrite(RELAY_PERISTALTICA_2, LOW);
  else digitalWrite(RELAY_PERISTALTICA_2, HIGH);

  // pH alto: bajar pH
  if (phValue > 8.0) digitalWrite(RELAY_PERISTALTICA_1, LOW);
  else if (phValue < idealPHMin) digitalWrite(RELAY_PERISTALTICA_1, LOW);
  else digitalWrite(RELAY_PERISTALTICA_1, HIGH);

  // EC baja: agregar nutrientes (tomates cherry)
  if (ecValue < idealECMin) {
    digitalWrite(RELAY_PERISTALTICA_3, LOW);
  } else {
    digitalWrite(RELAY_PERISTALTICA_3, HIGH);
  }

  delay(5000);
}
