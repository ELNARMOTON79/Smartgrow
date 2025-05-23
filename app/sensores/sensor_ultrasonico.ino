const int trigPin = 2;
const int echoPin = 5;

// Velocidad del sonido en el aire en cm/us (0.034 cm/us)
const float velocidadSonido = 0.034;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  // Disparo del pulso ultrasónico
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Medición del tiempo de eco
  long duracion = pulseIn(echoPin, HIGH);

  // Cálculo de la distancia en cm
  float distancia = (duracion * velocidadSonido) / 2.0;

  // Filtro para evitar mediciones erráticas
  if (distancia >= 2 && distancia <= 400) { // Rango válido del sensor
    Serial.print("Distancia: ");
    Serial.print(distancia);
    Serial.println(" cm");
  } else {
    Serial.println("Medición fuera de rango");
  }
  
  delay(200); // Pequeña pausa para estabilidad
}
