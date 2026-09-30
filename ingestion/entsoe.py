import os
from pathlib import Path
import time
from datetime import date, datetime, timedelta
from datetime import time as dtime
from zoneinfo import ZoneInfo
import requests
from dotenv import load_dotenv
import argparse

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv()
API_KEY = os.getenv("ENTSOE_API_KEY")
print("Key loaded:", API_KEY is not None)

ENTSOE_URL = "https://web-api.tp.entsoe.eu/api"
FINLAND = "10YFI-1--------U"

MARKET_TZ = ZoneInfo("Europe/Brussels")
UTC = ZoneInfo("UTC")


def market_day_range(day):
    """Return the UTC start and end of one market day, as yyyyMMddHHmm strings."""
    start = datetime.combine(day, dtime(0, 0), tzinfo=MARKET_TZ).astimezone(UTC)
    end = datetime.combine(day + timedelta(days=1), dtime(0, 0), tzinfo=MARKET_TZ).astimezone(UTC)
    return start.strftime("%Y%m%d%H%M"), end.strftime("%Y%m%d%H%M")


def fetch_day(day):
    period_start, period_end = market_day_range(day)
    params = {
        "securityToken": API_KEY,
        "documentType": "A44",
        "in_Domain": FINLAND,
        "out_Domain": FINLAND,
        "periodStart": period_start,
        "periodEnd": period_end,
    }
    response = requests.get(ENTSOE_URL, params=params, timeout=60)
    response.raise_for_status()
    return response.text

def save_raw(xml_text, day):
    path = (
        PROJECT_ROOT / "data" / "raw" / "entsoe" / "day_ahead_prices"
        / f"date={day}"
        / "data.xml"
    )
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(xml_text)

    return path

def main():
    parser = argparse.ArgumentParser(description="Ingest ENTSO-E day-ahead prices for Finland.")
    parser.add_argument("--start", required=True, help="First market day, YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="Last market day (inclusive), YYYY-MM-DD")
    args = parser.parse_args()

    day = date.fromisoformat(args.start)
    end_day = date.fromisoformat(args.end)

    while day <= end_day:
        xml_text = fetch_day(day)
        path = save_raw(xml_text, day)
        print(f"{day}: saved to {path}")
        time.sleep(1)
        day += timedelta(days=1)


if __name__ == "__main__":
    main()