{{ config(materialized='table') }}
WITH consumption AS (
    SELECT 
    date_trunc('hour', time) AS hour, 
    AVG(consumption_mw) AS avg_consumption_mw
    FROM {{ ref('stg_consumption') }} 
    GROUP BY hour
),
prices AS (
    SELECT 
    date_trunc('hour', time) AS hour, 
    AVG(price_eur_mwh) AS avg_price_eur_mwh
    FROM {{ ref('stg_prices') }}
    GROUP BY hour
),
weather AS (
    SELECT
    time as hour,
    AVG(temperature_c) AS avg_temperature_c,
    AVG(wind_speed_ms) AS avg_wind_speed_ms
    FROM {{ ref('stg_weather') }}
    GROUP by hour
)
SELECT 
consumption.hour AS hour,
ROUND(avg_consumption_mw, 2) AS avg_consumption_mw,
ROUND(avg_price_eur_mwh, 2) AS avg_price_eur_mwh,
ROUND(avg_temperature_c, 2) AS avg_temperature_c,
ROUND(avg_wind_speed_ms, 2) AS avg_wind_speed_ms
FROM consumption
JOIN prices ON consumption.hour = prices.hour
JOIN weather ON consumption.hour = weather.hour
ORDER BY hour