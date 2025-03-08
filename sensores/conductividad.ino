#define TdsSensorPin A0
#define VREF 5.0   // Voltaje de referencia del Arduino (5V o 3.3V)
#define SCOUNT 30  // Cantidad de muestras para estabilización

int analogBuffer[SCOUNT]; // Array de muestras
int analogBufferIndex = 0;
float temperature = 25; // Temperatura del agua en grados Celsius (ajusta según necesidad)

void setup() {
  Serial.begin(9600);
  pinMode(TdsSensorPin, INPUT);
}

void loop() {
  static unsigned long previousMillis = 0;
  const long interval = 500;  // Lectura cada 500 ms

  if (millis() - previousMillis >= interval) {
    previousMillis = millis();

    // Leer múltiples valores y promediar
    int sum = 0;
    for (int i = 0; i < SCOUNT; i++) {
      analogBuffer[i] = analogRead(TdsSensorPin);
      sum += analogBuffer[i];
    }
    int analogValue = sum / SCOUNT; // Promedio de las lecturas

    // Convertir a voltaje
    float voltage = analogValue * (VREF / 1024.0);

    // Conversión de voltaje a TDS en PPM (fórmula estándar)
    float tdsValue = (133.42 * voltage * voltage * voltage - 
                      255.86 * voltage * voltage + 
                      857.39 * voltage) * (1.0 + 0.02 * (temperature - 25));

    Serial.print("TDS: ");
    Serial.print(tdsValue);
    Serial.println(" ppm");

    delay(1000);
  }
}
