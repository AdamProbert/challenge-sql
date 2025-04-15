-- Solution for intermediate challenge #1 on basic JOIN operations
SELECT
    p.name AS pokemon_name,
    p.type,
    p.cp,
    t.name AS trainer_name
FROM
    pokemon p
    JOIN trainers t ON p.trainer_id = t.trainer_id
ORDER BY
    trainer_name,
    cp DESC;
