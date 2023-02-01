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
LIMIT 10;
