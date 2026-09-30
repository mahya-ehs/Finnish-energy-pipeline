import duckdb

con = duckdb.connect()  # a temporary in-memory database

result = con.sql("""
    SELECT date, station, COUNT(*) AS rows
    FROM read_parquet('data/staging/fmi/weather/*/*/data.parquet')
    GROUP BY date, station
    ORDER BY date, station
""")
print(result)