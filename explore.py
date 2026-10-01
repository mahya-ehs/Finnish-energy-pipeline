import duckdb

con = duckdb.connect("data/warehouse.duckdb")

print(con.sql("""
    SELECT
        date_trunc('hour', time) AS hour,
        AVG(consumption_mw)      AS consumption_mw
    FROM stg_consumption
    GROUP BY hour
    ORDER BY hour
    LIMIT 5
"""))


print(con.sql("SELECT * FROM fct_hourly_energy ORDER BY hour LIMIT 24"))

print(con.sql("""
    SELECT station, COUNT(*) AS missing_wind_hours
    FROM stg_weather
    WHERE wind_speed_ms IS NULL
    GROUP BY station
"""))

con.close()
