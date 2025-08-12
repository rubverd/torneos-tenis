USE torneos_tenis;

DELIMITER $$

-- =============================================
-- Procedimiento: asignar puntos a jugadores al finalizar un partido
-- =============================================
CREATE PROCEDURE asignar_puntos_partido(IN partido_id INT)
BEGIN
    DECLARE torneoId INT;
    DECLARE ganadorId INT;
    DECLARE perdedorId INT;
    DECLARE fasePartido ENUM('fase_grupos', 'octavos', 'cuartos', 'semifinal', 'final');
    DECLARE puntosGanador INT;
    DECLARE puntosPerdedor INT;

    -- 1. Obtener datos del partido
    SELECT torneo_id, ganador_id, perdedor_id, fase
    INTO torneoId, ganadorId, perdedorId, fasePartido
    FROM partidos
    WHERE id = partido_id;

    -- 2. Determinar puntos según la fase
    CASE fasePartido
        WHEN 'cuartos' THEN
            SET puntosPerdedor = 400;
        WHEN 'semifinal' THEN
            SET puntosPerdedor = 800;
        WHEN 'final' THEN
            SET puntosGanador = 2000;
            SET puntosPerdedor = 1300;
    END CASE;

    -- 3. Insertar o actualizar puntuaciones históricas
    INSERT INTO puntuaciones_torneo (torneo_id, jugador_id, puntos)
    VALUES (torneoId, ganadorId, puntosGanador)
    ON DUPLICATE KEY UPDATE puntos = puntos + VALUES(puntos);

    INSERT INTO puntuaciones_torneo (torneo_id, jugador_id, puntos)
    VALUES (torneoId, perdedorId, puntosPerdedor)
    ON DUPLICATE KEY UPDATE puntos = puntos + VALUES(puntos);

    -- 4. Actualizar puntos totales globales
    UPDATE jugadores SET puntos_totales = puntos_totales + puntosGanador WHERE id = ganadorId;
    UPDATE jugadores SET puntos_totales = puntos_totales + puntosPerdedor WHERE id = perdedorId;
END$$

-- =============================================
-- Trigger: ejecutar el procedimiento cuando se asigne ganador y perdedor
-- =============================================
CREATE TRIGGER trg_asignar_puntos_despues_ganador
AFTER UPDATE ON partidos
FOR EACH ROW
BEGIN
    IF OLD.ganador_id IS NULL AND NEW.ganador_id IS NOT NULL
       AND OLD.perdedor_id IS NULL AND NEW.perdedor_id IS NOT NULL THEN
        CALL asignar_puntos_partido(NEW.id);
    END IF;
END$$

DELIMITER ;
