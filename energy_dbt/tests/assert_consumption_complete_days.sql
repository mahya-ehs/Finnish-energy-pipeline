SELECT
    CAST(time AT TIME ZONE 'UTC' AS DATE)  AS day,
    SUM(resolution_minutes)                AS total_minutes
FROM {{ ref('stg_consumption') }}
GROUP BY day
HAVING total_minutes <> 1440
   AND day NOT IN (
       SELECT CAST(day AS DATE)
       FROM {{ ref('known_source_gaps') }}
       WHERE source = 'fingrid_consumption'
   )