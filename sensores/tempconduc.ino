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
#define RELAY_PERISTALTICA_3 6  // IN5 D6 nutrientes

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

// --- Variables para rangos ideales ---
float idealPHMin = 5.5;
float idealPHMax = 7.5;
float idealECMin = 1.2;
float idealECMax = 2.5;

void setup() {
  Serial.begin(9600);
  sensors.begin();

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(RELAY_PERISTALTICA_1, OUTPUT);
  pinMode(RELAY_PERISTALTICA_2, OUTPUT);
  pinMode(RELAY_PERISTALTICA_3, OUTPUT);

  // Inicializa relays en estado apagado (HIGH si relays activos en LOW)
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

  long duracion = pulseIn(ECHO_PIN, HIGH, 30000); // Timeout: 30ms

  if (duracion == 0) return -1;

  float distancia = duracion * 0.034 / 2;
  distancia += OFFSET_CALIBRACION_CM;
  return distancia;
}

void loop() {
  // --- Medición de Nivel de Agua ---
  float distancia = medirDistancia();
  float nivelAgua = ALTURA_SENSOR_CM - distancia;

  bool alertaNivel = false;
  if (distancia < 0) {
    nivelAgua = 0;
    alertaNivel = true;
  } else {
    if (nivelAgua < 0) nivelAgua = 0;
    if (nivelAgua < NIVEL_MINIMO_CM) {
      alertaNivel = true;
    }
  }

  // --- Medición de Temperatura ---
  sensors.requestTemperatures();
  float temperatura = sensors.getTempCByIndex(0);

  // --- Medición de EC ---
  int analogValueEC = analogRead(EC_PIN);
  float voltageEC = (analogValueEC / ADC_RESOLUTION) * VREF;
  float ecValue = (voltageEC / calibrationConstant) * (1.0 + 0.0185 * (temperatura - 25.0));  // mS/cm

  // --- Medición de pH ---
  int rawPH = analogRead(PH_PIN);
  float voltagePH = rawPH * (5.0 / 1023.0);
  float phValue = -6.475 * voltagePH + 25.99;

  // --- RESPONDER A COMANDOS POR SERIAL ---
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "TEST") {
      Serial.println("OK");
    } else if (cmd == "READ_SENSORS") {
      // Enviar datos en formato JSON
      Serial.print("{");
      Serial.print("\"nivelAgua_cm\":"); Serial.print(nivelAgua, 2); Serial.print(",");
      Serial.print("\"temp_C\":"); Serial.print(temperatura, 2); Serial.print(",");
      Serial.print("\"EC_mS_cm\":"); Serial.print(ecValue, 2); Serial.print(",");
      Serial.print("\"pH\":"); Serial.print(phValue, 2); Serial.print(",");
      Serial.print("\"alertaNivel\":"); Serial.print(alertaNivel ? 1 : 0);
      Serial.println("}");
    } else if (cmd.startsWith("ACTIVATE_PUMP")) {
      int pumpNumber = cmd.substring(14).toInt();
      if (pumpNumber == 1) {
        digitalWrite(RELAY_PERISTALTICA_1, LOW);
      } else if (pumpNumber == 2) {
        digitalWrite(RELAY_PERISTALTICA_2, LOW);
      } else if (pumpNumber == 3) {
        digitalWrite(RELAY_PERISTALTICA_3, LOW);
      }
    } else if (cmd.startsWith("DEACTIVATE_PUMP")) {
      int pumpNumber = cmd.substring(17).toInt();
      if (pumpNumber == 1) {
        digitalWrite(RELAY_PERISTALTICA_1, HIGH);
      } else if (pumpNumber == 2) {
        digitalWrite(RELAY_PERISTALTICA_2, HIGH);
      } else if (pumpNumber == 3) {
        digitalWrite(RELAY_PERISTALTICA_3, HIGH);
      }
    }
  }

  // --- Salida Serial periódica para monitoreo humano ---
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

  // --- Control de bombas basado en rangos ideales ---

  // Control de pH (ideal)
  if (phValue < idealPHMin) {
    digitalWrite(RELAY_PERISTALTICA_1, LOW);  // Bajar pH
  } else {
    digitalWrite(RELAY_PERISTALTICA_1, HIGH);
  }

  if (phValue > idealPHMax) {
    digitalWrite(RELAY_PERISTALTICA_2, LOW);  // Subir pH
  } else {
    digitalWrite(RELAY_PERISTALTICA_2, HIGH);
  }

  // Control de emergencia por pH fuera de rango crítico
  if (phValue < 6.0) {
    digitalWrite(RELAY_PERISTALTICA_2, LOW);  // Subir pH urgentemente
  }

  if (phValue > 8.0) {
    digitalWrite(RELAY_PERISTALTICA_1, LOW);  // Bajar pH urgentemente
  }

  // Control de EC (nutrientes)
  if (ecValue < idealECMin) {
    digitalWrite(RELAY_PERISTALTICA_3, LOW);  // Agregar nutrientes
  } else {
    digitalWrite(RELAY_PERISTALTICA_3, HIGH);
  }

  delay(5000);  // Espera entre ciclos
}
