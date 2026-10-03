SELECT 
time, price_eur_mwh, resolution_minutes, date AS market_date
FROM {{ source('pipeline', 'entsoe_prices') }}