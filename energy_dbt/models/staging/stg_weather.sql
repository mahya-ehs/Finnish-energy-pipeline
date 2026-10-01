SELECT
time, 
station, 
MAX(CASE WHEN parameter = 'TA_PT1H_AVG' THEN value END) AS temperature_c, 
MAX(CASE WHEN parameter = 'WS_PT1H_AVG' THEN value END) AS wind_speed_ms
FROM read_parquet('../data/staging/fmi/weather/*/*/data.parquet')
GROUP BY time, station