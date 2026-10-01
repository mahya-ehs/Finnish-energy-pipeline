from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime, timedelta

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "entsoe" / "day_ahead_prices"
STAGING_DIR = PROJECT_ROOT / "data" / "staging" / "entsoe" / "day_ahead_prices"
NS = {"ns": "urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:3"}

TIME_SLOTS = ({
    "PT15M": 15, 
    "PT60M": 60,
    "PT1H" : 60,
})


def parse_file(xml_path):
    root = ET.parse(xml_path).getroot()
    periods = root.findall(".//ns:Period", NS)
    if not periods:
        raise ValueError(f"No Period found in {xml_path}")

    rows = []
    for period in periods:
        start = datetime.fromisoformat(period.find("ns:timeInterval/ns:start", NS).text)
        end = datetime.fromisoformat(period.find("ns:timeInterval/ns:end", NS).text)
        resolution = period.find("ns:resolution", NS).text
        minutes = TIME_SLOTS[resolution]
        step = timedelta(minutes=minutes)

        prices = {}
        for point in period.findall("ns:Point", NS):
            position = int(point.find("ns:position", NS).text)
            price = float(point.find("ns:price.amount", NS).text)
            prices[position] = price

        n_slots = int((end - start) / step)
        last_price = None
        for position in range(1, n_slots + 1):
            if position in prices:
                last_price = prices[position]
            rows.append({
                "time": start + (position - 1) * step,
                "price_eur_mwh": last_price,
                "resolution_minutes": minutes,
            })

    return rows

def save_rows(rows, day):
    path = STAGING_DIR / f"date={day}" / "data.parquet"
    path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(rows)
    df["time"] = pd.to_datetime(df["time"], utc=True)
    df.to_parquet(path, index=False)
    return path

def main():
    files = sorted(RAW_DIR.glob("date=*/data.xml"))
    for f in files:
        day = f.parent.name.split("=")[1]
        rows = parse_file(f)
        path = save_rows(rows, day)
        print(f"{day}: {len(rows)} rows -> {path}")
      
 
if __name__=="__main__":
    main()