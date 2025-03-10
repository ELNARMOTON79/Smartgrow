-- Tabla Luz
CREATE TABLE IF NOT EXISTS `Luz` (
  `id` bigint NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `fecha` date DEFAULT NULL,
  `hora` time NOT NULL,
  `estado` varchar(500) NOT NULL
);

-- Tabla NivelAgua
CREATE TABLE IF NOT EXISTS `NivelAgua` (
  `id` bigint NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `fecha` date DEFAULT NULL,
  `hora` time NOT NULL,
  `id_sensor` bigint NOT NULL,
  `valor` decimal(10, 2) NOT NULL
);

CREATE INDEX `idx_nivel_agua_id_sensor` ON `NivelAgua` (`id_sensor`);

-- Tabla ConductividadElectrica
CREATE TABLE IF NOT EXISTS `ConductividadElectrica` (
  `id` bigint NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `fecha` date DEFAULT NULL,
  `hora` time NOT NULL,
  `id_sensor` bigint NOT NULL,
  `valor` decimal(10, 2) NOT NULL
);

CREATE INDEX `idx_conductividad_id_sensor` ON `ConductividadElectrica` (`id_sensor`);

-- Tabla PH
CREATE TABLE IF NOT EXISTS `PH` (
  `id` bigint NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `fecha` date DEFAULT NULL,
  `hora` time NOT NULL,
  `valor` decimal(10, 2) NOT NULL,
  `id_sensor` bigint NOT NULL
);

CREATE INDEX `idx_ph_id_sensor` ON `PH` (`id_sensor`);

-- Tabla Temperatura
CREATE TABLE IF NOT EXISTS `Temperatura` (
  `id` bigint NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `fecha` date DEFAULT NULL,
  `hora` time NOT NULL,
  `id_sensor` bigint NOT NULL,
  `valor` decimal(10, 2) NOT NULL
);

CREATE INDEX `idx_temperatura_id_sensor` ON `Temperatura` (`id_sensor`);

-- Tabla Ventiladores
CREATE TABLE IF NOT EXISTS `Ventiladores` (
  `id` bigint NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `fecha` date DEFAULT NULL,
  `hora` time NOT NULL,
  `estado` varchar(500) NOT NULL,
  `temperatura` decimal(10, 2) NOT NULL
);

CREATE INDEX `idx_ventiladores_temperatura` ON `Ventiladores` (`temperatura`);

-- Tabla Humedad
CREATE TABLE IF NOT EXISTS `Humedad` (
  `id` bigint NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `porcentaje` decimal(10, 2) NOT NULL,
  `fecha` date DEFAULT NULL,
  `hora` time NOT NULL,
  `sensor_id` bigint NOT NULL
);

CREATE INDEX `idx_humedad_sensor_id` ON `Humedad` (`sensor_id`);

-- Tabla Oxigeno
CREATE TABLE IF NOT EXISTS `Oxigeno` (
  `id` bigint NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `fecha` date DEFAULT NULL,
  `hora` time NOT NULL,
  `valor` decimal(10, 2) NOT NULL,
  `id_sensor` bigint NOT NULL
);

CREATE INDEX `idx_oxigeno_id_sensor` ON `Oxigeno` (`id_sensor`);

-- Tabla Sensores
CREATE TABLE IF NOT EXISTS `Sensores` (
  `id` bigint NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `sensor` varchar(500) NOT NULL,
  `tipo_sensor` varchar(500) NOT NULL
);

-- Tabla Bomba
CREATE TABLE IF NOT EXISTS `Bomba` (
  `id` bigint NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `fecha` date DEFAULT NULL,
  `hora` time NOT NULL,
  `estado` varchar(500) NOT NULL
);

-- Restricciones de clave foránea
ALTER TABLE `NivelAgua` ADD CONSTRAINT `fk_nivel_agua_sensor` FOREIGN KEY (`id_sensor`) REFERENCES `Sensores` (`id`);
ALTER TABLE `ConductividadElectrica` ADD CONSTRAINT `fk_conductividad_sensor` FOREIGN KEY (`id_sensor`) REFERENCES `Sensores` (`id`);
ALTER TABLE `PH` ADD CONSTRAINT `fk_ph_sensor` FOREIGN KEY (`id_sensor`) REFERENCES `Sensores` (`id`);
ALTER TABLE `Temperatura` ADD CONSTRAINT `fk_temperatura_sensor` FOREIGN KEY (`id_sensor`) REFERENCES `Sensores` (`id`);
ALTER TABLE `Humedad` ADD CONSTRAINT `fk_humedad_sensor` FOREIGN KEY (`sensor_id`) REFERENCES `Sensores` (`id`);
ALTER TABLE `Oxigeno` ADD CONSTRAINT `fk_oxigeno_sensor` FOREIGN KEY (`id_sensor`) REFERENCES `Sensores` (`id`);