-- Tabla de sensores
CREATE TABLE sensores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL, -- Ej: temperatura, humedad, luz, etc.
    descripcion TEXT
);

-- Tabla de historial (almacena todos los valores de sensores por registro)
CREATE TABLE historial (
    id INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    temperatura FLOAT,
    ph FLOAT,
    conductividad FLOAT,
    nivel_agua FLOAT
);

-- Tabla de notificaciones
CREATE TABLE notificaciones (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sensor_id INT, -- Relaciona la notificación con un sensor específico
    mensaje TEXT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    leida BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (sensor_id) REFERENCES sensores(id)
);

-- Inserts para la tabla sensores
INSERT INTO sensores (nombre, tipo, descripcion) VALUES
('Sensor de Temperatura', 'temperatura', 'Sensor para medir la temperatura del ambiente o solución.'),
('Sensor de pH', 'ph', 'Sensor para medir el nivel de pH de la solución.'),
('Sensor de Electroconductividad', 'electroconductividad', 'Sensor para medir la conductividad eléctrica de la solución.'),
('Sensor Ultrasónico', 'ultrasonico', 'Sensor para medir la distancia o nivel de líquido mediante ultrasonido.');

-- Ejemplo de insert para historial
INSERT INTO historial (fecha, hora, temperatura, ph, conductividad, nivel_agua) VALUES
('2024-06-01', '08:00:00', 22.5, 6.2, 1300, 12.5),
('2024-06-01', '12:00:00', 24.1, 6.3, 1400, 12.7),
('2024-06-02', '08:00:00', 21.8, 6.1, 1250, 12.4),
('2024-06-02', '12:00:00', 23.0, 6.4, 1350, 12.6);
