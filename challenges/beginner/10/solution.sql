-- Solution for beginner challenge #10 on column aliases
SELECT
    name AS "Pokemon Name",
    type AS "Pokemon Type",
    hp + defense AS "Defensive Strength",
    attack + speed AS "Offensive Strength"
FROM
    pokemon
ORDER BY
    "Offensive Strength" DESC;
