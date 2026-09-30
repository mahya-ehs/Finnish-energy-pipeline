import requests
from pathlib import Path
import argparse
import time
from datetime import date, timedelta

# found from https://www.ilmatieteenlaitos.fi/
STATIONS = {
    "helsinki": 100971,
    "tampere": 101124,
    "turku": 101065,
    "vaasa": 101462,
    "oulu": 101786,
    "rovaniemi": 137190,
}
FMI_URL = "https://opendata.fmi.fi/wfs"
PROJECT_ROOT = Path(__file__).resolve().parent.parent


# Fetch one day of hourly observations for one station. Return the raw XML text.
def fetch_day(fmisid, day):
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "getFeature",
        "storedquery_id": "fmi::observations::weather::hourly::simple",
        "fmisid": fmisid,
        "starttime": f"{day}T00:00:00Z",
        "endtime": f"{day}T23:00:00Z",
    }
    response = requests.get(FMI_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.text


def save_raw(xml_text, day, station):
    path = (
        PROJECT_ROOT / "data" / "raw" / "fmi" / "weather"
        / f"date={day}" / f"station={station}"
        / "data.xml"
    )
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(xml_text)

    return path


def main():
    parser = argparse.ArgumentParser(description="Ingest FMI hourly weather observations.")
    parser.add_argument("--start", required=True, help="First day, YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="Last day (inclusive), YYYY-MM-DD")
    args = parser.parse_args()

    day = date.fromisoformat(args.start)
    end_day = date.fromisoformat(args.end)

    while day <= end_day:
        for station, fmisid in STATIONS.items():
            xml_text = fetch_day(fmisid, day)
            path = save_raw(xml_text, day, station)
            print(f"{day} {station}: saved to {path}")
            time.sleep(1)
        day += timedelta(days=1)
 
if __name__ == "__main__":
    main()

