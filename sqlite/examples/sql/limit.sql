.echo on
.mode column
.headers on
.nullvalue NULL

SELECT
        *
FROM
        foods
WHERE
        name LIKE 'B%'
ORDER BY type_id desc, name
-- LIMIT 1 OFFSET 2;
LIMIT 2, 1;
