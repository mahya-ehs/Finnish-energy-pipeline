SELECT time, station, COUNT(*) AS n
FROM {{ ref('stg_weather') }}
GROUP BY time, station
HAVING COUNT(*) > 1