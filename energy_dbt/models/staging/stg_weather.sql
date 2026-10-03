SELECT
time - INTERVAL 1 HOUR AS time, 
station, 
MAX(CASE WHEN parameter = 'TA_PT1H_AVG' THEN value END) AS temperature_c, 
MAX(CASE WHEN parameter = 'WS_PT1H_AVG' THEN value END) AS wind_speed_ms
FROM {{ source('pipeline', 'fmi_weather') }}
GROUP BY time, station