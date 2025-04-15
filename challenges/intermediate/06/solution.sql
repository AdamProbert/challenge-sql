-- Solution for intermediate challenge #6 on subqueries
SELECT
    t.name AS trainer_name,
    COUNT(*) AS strong_pokemon_count,
    ROUND(AVG(p.cp), 2) AS strong_pokemon_avg_cp
FROM
    pokemon p
    JOIN trainers t ON p.trainer_id = t.trainer_id
WHERE
    p.cp > (
        SELECT
            AVG(cp)
        FROM
            pokemon
    )
GROUP BY
    t.name
ORDER BY
    strong_pokemon_count DESC;
