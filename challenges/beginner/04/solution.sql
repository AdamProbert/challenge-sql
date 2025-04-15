-- Solution for beginner challenge #4 on ORDER BY
SELECT
    name,
    type,
    cp
FROM
    pokemon
ORDER BY
    type ASC,
    cp DESC;
