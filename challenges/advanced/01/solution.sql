-- Solution for advanced subquery & aggregation challenge
SELECT
    pt.type_name AS pokemon_type,
    COUNT(p.pokemon_id) AS pokemon_count,
    ROUND(AVG(p.cp), 2) AS avg_cp
FROM
    pokemon_types pt
    JOIN pokemon p ON pt.type_id = p.type_id
    OR pt.type_id = p.secondary_type_id
GROUP BY
    pt.type_name
HAVING
    AVG(p.cp) > (
        SELECT
            AVG(cp)
        FROM
            pokemon
    )
ORDER BY
    avg_cp DESC;
