-- Solution for intermediate challenge #2 on LEFT JOIN
SELECT
    p.name AS pokemon_name,
    p.type,
    p.cp
FROM
    pokemon p
    LEFT JOIN trainers t ON p.trainer_id = t.trainer_id
WHERE
    p.trainer_id IS NULL
ORDER BY
    p.cp DESC;
