.echo on
.mode column
.headers on
.nullvalue NULL

/*
SELECT 
        * 
FROM 
        foods
WHERE 
        name='JujyFruit' AND 
        type_id=9;

*/

SELECT
        id,
        name
FROM
        foods
WHERE
        name LIKE 'J%';
