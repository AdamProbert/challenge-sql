-- Solution for beginner challenge #8 on NULL values
SELECT
    pokemon_id,
    name,
    type,
    evolution_level,
    evolution_stone
FROM
    pokemon
WHERE
    evolution_level IS NULL
    OR evolution_stone IS NULL
ORDER BY
    name;
