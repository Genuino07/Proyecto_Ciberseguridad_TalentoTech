-- 1. Impacto Financiero por Tipo de Ataque 
SELECT attack_type, ROUND(SUM(financial_loss_in_million_), 2) as total_perdida
FROM amenazas
GROUP BY attack_type
ORDER BY total_perdida DESC;

-- 2. Industrias más vulnerables por número de usuarios afectados
SELECT target_industry, SUM(number_of_affected_users) as total_usuarios
FROM amenazas
GROUP BY target_industry
ORDER BY total_usuarios DESC;

-- 3. Eficiencia de los mecanismos de defensa (Tiempo de resolución promedio)
SELECT defense_mechanism_used, AVG(incident_resolution_time_in_hours) as tiempo_promedio
FROM amenazas
GROUP BY defense_mechanism_used
ORDER BY tiempo_promedio ASC;

--4. ¿Cuál es el costo promedio de pérdida cuando el ataque proviene de un "Nation-state" vs "Hacker Group"?
SELECT 
    attack_source, 
    security_vulnerability_type,
    COUNT(*) as frecuencia,
    ROUND(AVG(financial_loss_in_million_), 2) as perdida_promedio_millones
FROM amenazas
GROUP BY attack_source, security_vulnerability_type
ORDER BY perdida_promedio_millones DESC;

-- Industrias con pérdidas mayores a 50M y más de 500,000 usuarios afectados
SELECT 
    target_industry, 
    COUNT(*) as total_incidentos,
    ROUND(SUM(financial_loss_in_million_), 2) as perdida_total,
    SUM(number_of_affected_users) as total_usuarios_afectados
FROM amenazas
GROUP BY target_industry
HAVING perdida_total > 50 AND total_usuarios_afectados > 500000
ORDER BY perdida_total DESC;


-- Ranking de mecanismos de defensa según su velocidad de respuesta ante ataques de "Ransomware"
SELECT 
    defense_mechanism_used, 
    MIN(incident_resolution_time_in_hours) as tiempo_minimo,
    MAX(incident_resolution_time_in_hours) as tiempo_maximo,
    ROUND(AVG(incident_resolution_time_in_hours), 2) as tiempo_promedio
FROM amenazas
WHERE attack_type = 'Ransomware'
GROUP BY defense_mechanism_used
ORDER BY tiempo_promedio ASC;


-- ¿Cuál es la pérdida promedio por industria y tipo de ataque? 
-- (Ayuda a priorizar presupuestos de seguridad)
SELECT 
    target_industry, 
    attack_type, 
    ROUND(AVG(financial_loss_in_million_), 2) as perdida_promedio,
    COUNT(*) as cantidad_incidentes
FROM amenazas
GROUP BY target_industry, attack_type
ORDER BY perdida_promedio DESC
LIMIT 15;



-- Vulnerabilidades más explotadas por fuentes de ataque profesionales
SELECT 
    security_vulnerability_type, 
    attack_source,
    COUNT(*) as frecuencia,
    SUM(number_of_affected_users) as total_afectados
FROM amenazas
WHERE attack_source IN ('Nation-state', 'Hacker Group')
GROUP BY security_vulnerability_type, attack_source
ORDER BY frecuencia DESC;


-- ¿Qué mecanismos de defensa resuelven incidentes más rápido?
SELECT 
    defense_mechanism_used, 
    ROUND(AVG(incident_resolution_time_in_hours), 1) as horas_promedio,
    MAX(incident_resolution_time_in_hours) as tiempo_maximo_detectado
FROM amenazas
GROUP BY defense_mechanism_used
ORDER BY horas_promedio ASC;


-- Evolución anual de las pérdidas y el alcance de los ataques
SELECT 
    year, 
    ROUND(SUM(financial_loss_in_million_), 2) as perdida_anual,
    SUM(number_of_affected_users) as usuarios_afectados_anual
FROM amenazas
GROUP BY year
ORDER BY year ASC;


-- RANKING 1: Países con mayor impacto financiero (Los más afectados)
SELECT country, 
       SUM(financial_loss_in_million_) as perdida_total,
       COUNT(*) as total_ataques
FROM amenazas
GROUP BY country
ORDER BY perdida_total DESC
LIMIT 10;

-- RANKING 2: Países "Mejor Preparados" 
-- (Basado en menor tiempo de respuesta promedio y uso de defensas avanzadas)
SELECT country, 
       ROUND(AVG(incident_resolution_time_in_hours), 2) as tiempo_respuesta_avg,
       COUNT(CASE WHEN defense_mechanism_used IN ('AI-based Detection', 'Encryption') THEN 1 END) as defensas_avanzadas
FROM amenazas
GROUP BY country
ORDER BY tiempo_respuesta_avg ASC
LIMIT 10;


