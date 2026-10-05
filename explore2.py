from pathlib import Path

import duckdb
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent
DB_PATH = PROJECT_ROOT / "data" / "warehouse.duckdb"
DOCS_DIR = PROJECT_ROOT / "docs"
DOCS_DIR.mkdir(exist_ok=True)

con = duckdb.connect(str(DB_PATH), read_only=True)

# 1. Price by wind speed
wind = con.sql("""
    SELECT ROUND(avg_wind_speed_ms) AS wind_ms,
           AVG(avg_price_eur_mwh)   AS avg_price,
           COUNT(*)                 AS hours
    FROM fct_hourly_energy
    GROUP BY wind_ms
    HAVING hours >= 50
    ORDER BY wind_ms
""").df()

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(wind["wind_ms"], wind["avg_price"])
ax.set_xlabel("Average wind speed (m/s)")
ax.set_ylabel("Average price (€/MWh)")
ax.set_title("Electricity price by wind speed")
fig.tight_layout()
fig.savefig(DOCS_DIR / "price_by_wind.png", dpi=150)

# 2. Consumption and price by temperature
temp = con.sql("""
    SELECT FLOOR(avg_temperature_c / 5) * 5  AS temp_from_c,
           AVG(avg_consumption_mw)           AS avg_consumption,
           AVG(avg_price_eur_mwh)            AS avg_price,
           COUNT(*)                          AS hours
    FROM fct_hourly_energy
    GROUP BY temp_from_c
    HAVING hours >= 50
    ORDER BY temp_from_c
""").df()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
ax1.plot(temp["temp_from_c"], temp["avg_consumption"], marker="o")
ax1.set_xlabel("Temperature (°C)")
ax1.set_ylabel("Average consumption (MW)")
ax1.set_title("Consumption by temperature")
ax2.plot(temp["temp_from_c"], temp["avg_price"], marker="o", color="tab:red")
ax2.set_xlabel("Temperature (°C)")
ax2.set_ylabel("Average price (€/MWh)")
ax2.set_title("Price by temperature")
fig.tight_layout()
fig.savefig(DOCS_DIR / "temperature.png", dpi=150)

# 3. Typical day (Finnish time)
day = con.sql("""
    SELECT hour(hour AT TIME ZONE 'Europe/Helsinki') AS hour_fi,
           AVG(avg_consumption_mw)                   AS avg_consumption,
           AVG(avg_price_eur_mwh)                    AS avg_price
    FROM fct_hourly_energy
    GROUP BY hour_fi
    ORDER BY hour_fi
""").df()

fig, ax1 = plt.subplots(figsize=(8, 4))
ax1.plot(day["hour_fi"], day["avg_consumption"], marker="o", label="Consumption")
ax1.set_xlabel("Hour of day (Finnish time)")
ax1.set_ylabel("Average consumption (MW)")
ax2 = ax1.twinx()
ax2.plot(day["hour_fi"], day["avg_price"], marker="o", color="tab:red", label="Price")
ax2.set_ylabel("Average price (€/MWh)")
ax1.set_title("A typical day: consumption vs price")
fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
fig.tight_layout()
fig.savefig(DOCS_DIR / "typical_day.png", dpi=150)

con.close()
print(f"Charts saved to {DOCS_DIR}")