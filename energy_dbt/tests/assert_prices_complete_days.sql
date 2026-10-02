SELECT
    market_date,
    SUM(resolution_minutes) AS total_minutes
FROM {{ ref('stg_prices') }}
GROUP BY market_date
HAVING total_minutes NOT IN (1380, 1440, 1500)