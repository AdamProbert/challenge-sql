-- Solution for beginner challenge #9 on calculated fields
SELECT
    name,
    type,
    (attack * 2) + defense + (speed / 2) AS battle_power
FROM
    pokemon
WHERE
    (attack * 2) + defense + (speed / 2) > 200
ORDER BY
    battle_power DESC;
