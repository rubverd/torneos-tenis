-- =============================================
-- Script de creación de tablas para gestor de torneos de tenis
-- Ranking basado en puntos acumulados en jugadores
-- =============================================

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS torneos_tenis;
USE torneos_tenis;

-- Eliminamos tablas en orden inverso de dependencias
DROP TABLE IF EXISTS puntuaciones_torneo;
DROP TABLE IF EXISTS partidos;
DROP TABLE IF EXISTS torneos;
DROP TABLE IF EXISTS jugadores;

-- =============================================
-- Tabla jugadores
-- =============================================
CREATE TABLE jugadores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100),
    puntos_totales INT DEFAULT 0
) ENGINE=InnoDB;

-- =============================================
-- Tabla torneos
-- =============================================
CREATE TABLE torneos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_inicio DATE,
    fecha_fin DATE
) ENGINE=InnoDB;

-- =============================================
-- Tabla partidos
-- =============================================
CREATE TABLE partidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    torneo_id INT NOT NULL,
    jugador1_id INT NOT NULL,
    jugador2_id INT NOT NULL,
    ganador_id INT NULL,
    perdedor_id INT NULL,
    fecha DATE,
    fase ENUM('fase_grupos', 'octavos', 'cuartos', 'semifinal', 'final') NOT NULL DEFAULT 'fase_grupos',
    FOREIGN KEY (torneo_id) REFERENCES torneos(id) ON DELETE CASCADE,
    FOREIGN KEY (jugador1_id) REFERENCES jugadores(id),
    FOREIGN KEY (jugador2_id) REFERENCES jugadores(id),
    FOREIGN KEY (ganador_id) REFERENCES jugadores(id),
    FOREIGN KEY (perdedor_id) REFERENCES jugadores(id)
) ENGINE=InnoDB;

-- =============================================
-- Tabla puntuaciones por torneo (histórico)
-- =============================================
CREATE TABLE puntuaciones_torneo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    torneo_id INT NOT NULL,
    jugador_id INT NOT NULL,
    puntos INT NOT NULL,
    UNIQUE (torneo_id, jugador_id),
    FOREIGN KEY (torneo_id) REFERENCES torneos(id) ON DELETE CASCADE,
    FOREIGN KEY (jugador_id) REFERENCES jugadores(id)
) ENGINE=InnoDB;

-- =============================================
-- Índices 
-- =============================================
CREATE INDEX idx_jugador_username ON jugadores(username);
CREATE INDEX idx_torneo_nombre ON torneos(nombre);
CREATE INDEX idx_puntos_jugador ON puntuaciones_torneo(jugador_id);
