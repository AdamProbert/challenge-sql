-- Solution for beginner challenge #7 on BETWEEN and IN
SELECT
    pokemon_id,
    name,
    type,
    cp
FROM
    pokemon
WHERE
    cp BETWEEN 1000 AND 2000
    AND type IN ('Fire', 'Water', 'Grass')
ORDER BY
    type,
    cp DESC;
