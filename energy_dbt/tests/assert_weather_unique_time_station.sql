-- fails if too few weather stations reported in any hour.
-- Temperature: 6 stations
-- Wind: 5 stations (Tampere has no wind)
SELECT
    hour,
    temperature_station_count,
    wind_station_count
FROM {{ ref('fct_hourly_energy') }}
WHERE temperature_station_count < 4
   OR wind_station_count < 3