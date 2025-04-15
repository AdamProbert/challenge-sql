-- Solution for intermediate challenge #4 on HAVING clause
SELECT
    type,
    COUNT(*) AS pokemon_count,
    ROUND(AVG(cp), 2) AS avg_cp,
    MAX(cp) AS max_cp
FROM
    pokemon
GROUP BY
    type
HAVING
    COUNT(*) >= 3
    AND AVG(cp) > 1400
ORDER BY
    avg_cp DESC;
