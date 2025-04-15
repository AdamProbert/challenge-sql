-- Solution for beginner challenge #3 on AND, OR, NOT filtering
SELECT
    pokemon_id,
    name,
    type,
    cp
FROM
    pokemon
WHERE
    (
        type = 'Electric'
        OR type = 'Water'
    )
    AND cp > 1000;
