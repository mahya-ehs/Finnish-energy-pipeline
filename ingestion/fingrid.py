import os
import requests
import time
import json
from dotenv import load_dotenv
from pathlib import Path
import argparse
from datetime import date, timedelta

BASE_URL = "https://data.fingrid.fi/api"
DATASET_ID = 124
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# loading API key
load_dotenv()
API_KEY = os.getenv("FINGRID_API_KEY")
print("Key loaded:", API_KEY is not None)


# fetching data from a specific page and time
def fetch_page(start, end, page):
    url = f"{BASE_URL}/datasets/{DATASET_ID}/data"
    headers = {"x-api-key": API_KEY}
    params = {
        "startTime": start,
        "endTime": end,
        "format": "json",
        "page": page,
        "pageSize": 10000,
    }

    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

# fetching data from all pages
def fetch_all_pages(start, end):
    records = []
    page = 1

    while True:
        res = fetch_page(start, end, page)
        records.extend(res["data"])

        page = res["pagination"]["nextPage"]
        if page is None:
            break
        time.sleep(2) 
        
    return records


def save_raw_data(records, date):
    path = (
        PROJECT_ROOT / "data" / "raw" / "fingrid" / "consumption" 
        / f"date={date}"
        / "data.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        json.dump(records, f, indent=2)

    return path

def ingest_day(day):
    start = f"{day}T00:00:00Z"
    end = f"{day + timedelta(days=1)}T00:00:00Z"

    records = fetch_all_pages(start, end)
    path = save_raw_data(records, day)
    print(f"{day}: saved {len(records)} records to {path}")


def main():
    parser = argparse.ArgumentParser(description="Ingest Fingrid electricity consumption data.")
    parser.add_argument("--start", required=True, help="First day, YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="Last day (inclusive), YYYY-MM-DD")
    args = parser.parse_args()

    start_day = date.fromisoformat(args.start)
    end_day = date.fromisoformat(args.end)

    day = start_day
    while day <= end_day:
        ingest_day(day)
        day += timedelta(days=1)
        time.sleep(2)  


if __name__ == "__main__":
    main()