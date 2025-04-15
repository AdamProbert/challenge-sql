-- Solution for intermediate challenge #3 on aggregation
SELECT
    t.name AS trainer_name,
    COUNT(*) AS pokemon_count,
    SUM(p.cp) AS total_team_cp,
    ROUND(AVG(p.cp), 2) AS avg_cp
FROM
    pokemon p
    JOIN trainers t ON p.trainer_id = t.trainer_id
GROUP BY
    t.name
HAVING
    COUNT(*) >= 3
ORDER BY
    total_team_cp DESC;
