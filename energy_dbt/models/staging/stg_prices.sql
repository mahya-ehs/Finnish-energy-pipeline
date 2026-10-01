SELECT 
time, price_eur_mwh, resolution_minutes, date AS market_date
FROM read_parquet('../data/staging/entsoe/day_ahead_prices/*/data.parquet')