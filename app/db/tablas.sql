-- =============================================
-- Script de creación de tablas para gestor de torneos de tenis
-- Enfoque: Ranking basado en puntos acumulados en jugadores
-- =============================================

-- Usar la base de datos correspondiente
USE nombre_de_tu_base;

-- Eliminamos tablas en orden inverso de dependencias
DROP TABLE IF EXISTS puntuaciones_torneo;
DROP TABLE IF EXISTS partidos;
DROP TABLE IF EXISTS fases;
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
-- Tabla fases (cuartos, semifinales, final, etc.)
-- =============================================
CREATE TABLE fases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    torneo_id INT NOT NULL,
    nombre VARCHAR(50) NOT NULL, -- Ej: 'Cuartos de Final'
    orden INT NOT NULL, -- Para el orden cronológico
    FOREIGN KEY (torneo_id) REFERENCES torneos(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- =============================================
-- Tabla partidos
-- =============================================
CREATE TABLE partidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fase_id INT NOT NULL,
    jugador1_id INT NOT NULL,
    jugador2_id INT NOT NULL,
    ganador_id INT,
    fecha DATE,
    FOREIGN KEY (fase_id) REFERENCES fases(id) ON DELETE CASCADE,
    FOREIGN KEY (jugador1_id) REFERENCES jugadores(id),
    FOREIGN KEY (jugador2_id) REFERENCES jugadores(id),
    FOREIGN KEY (ganador_id) REFERENCES jugadores(id)
) ENGINE=InnoDB;

-- =============================================
-- Tabla puntuaciones por torneo (histórico)
-- =============================================
CREATE TABLE puntuaciones_torneo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    torneo_id INT NOT NULL,
    jugador_id INT NOT NULL,
    puntos INT NOT NULL,
    FOREIGN KEY (torneo_id) REFERENCES torneos(id) ON DELETE CASCADE,
    FOREIGN KEY (jugador_id) REFERENCES jugadores(id)
) ENGINE=InnoDB;

-- =============================================
-- Índices recomendados para rendimiento
-- =============================================
CREATE INDEX idx_jugador_username ON jugadores(username);
CREATE INDEX idx_torneo_nombre ON torneos(nombre);
CREATE INDEX idx_fase_orden ON fases(torneo_id, orden);
CREATE INDEX idx_partido_fase ON partidos(fase_id);
CREATE INDEX idx_puntos_jugador ON puntuaciones_torneo(jugador_id);
