-- Solution for beginner challenge #5 on LIMIT and OFFSET
SELECT
    name,
    type,
    cp
FROM
    pokemon
ORDER BY
    cp DESC
LIMIT
    5;
