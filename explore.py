import duckdb

con = duckdb.connect("data/warehouse.duckdb")


print(con.sql("""
    SELECT
        ROUND(avg_wind_speed_ms)          AS wind_ms,
        COUNT(*)                          AS hours,
        ROUND(AVG(avg_price_eur_mwh), 1)  AS avg_price
    FROM fct_hourly_energy
    GROUP BY wind_ms
    ORDER BY wind_ms
"""))
print(con.sql("""
    SELECT
        FLOOR(avg_temperature_c / 5) * 5   AS temp_from_c,
        COUNT(*)                           AS hours,
        ROUND(AVG(avg_consumption_mw))     AS avg_consumption,
        ROUND(AVG(avg_price_eur_mwh), 1)   AS avg_price
    FROM fct_hourly_energy
    GROUP BY temp_from_c
    ORDER BY temp_from_c
"""))

print(con.sql("""
    SELECT
        hour(hour AT TIME ZONE 'Europe/Helsinki')  AS hour_finland,
        ROUND(AVG(avg_consumption_mw))             AS avg_consumption,
        ROUND(AVG(avg_price_eur_mwh), 1)           AS avg_price
    FROM fct_hourly_energy
    GROUP BY hour_finland
    ORDER BY hour_finland
"""))

print(con.sql(
   """
    SELECT
        *
    FROM fct_hourly_energy
""" 
))
con.close()
