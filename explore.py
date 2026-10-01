import duckdb

con = duckdb.connect()  # a temporary in-memory database

result = con.sql("""
    SELECT date, station, COUNT(*) AS rows
    FROM read_parquet('data/staging/fmi/weather/*/*/data.parquet')
    GROUP BY date, station
    ORDER BY date, station
""")
print(result)

result = con.sql("""
    SELECT date, COUNT(*) AS slots, MIN(time) AS first_slot, MAX(time) AS last_slot,
           ROUND(AVG(price_eur_mwh), 2) AS avg_price
    FROM read_parquet('data/staging/entsoe/day_ahead_prices/*/data.parquet')
    GROUP BY date
    ORDER BY date
""")
print(result)