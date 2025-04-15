-- Solution for beginner challenge #6 on LIKE pattern matching
SELECT
    pokemon_id,
    name,
    type
FROM
    pokemon
WHERE
    name LIKE '%chu'
    OR name LIKE '%saur%';
