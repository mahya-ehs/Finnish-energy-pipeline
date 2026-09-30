from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "fmi" / "weather"
STAGING_DIR = PROJECT_ROOT / "data" / "staging" / "fmi" / "weather"
NS = {"BsWfs": "http://xml.fmi.fi/schema/wfs/2.0"}

def parse_file(xml_path, station):
    root = ET.parse(xml_path).getroot()
    rows = []
    for e in root.findall(".//BsWfs:BsWfsElement", NS):
        rows.append({
            "station": station,
            "time": e.find("BsWfs:Time", NS).text,
            "parameter": e.find("BsWfs:ParameterName", NS).text,
            "value": float(e.find("BsWfs:ParameterValue", NS).text),
        })
    return rows

def save_rows(rows, day, station):
    path = STAGING_DIR / f"date={day}" / f"station={station}" / "data.parquet"
    path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(rows)
    df["time"] = pd.to_datetime(df["time"], utc=True)
    df.to_parquet(path, index=False)
    return path

def main():
    files = sorted(RAW_DIR.glob("date=*/station=*/data.xml"))

    for f in files:
        station = (f.parent.name).split("=")[1]
        day = (f.parent.parent.name).split("=")[1]
        rows = parse_file(f, station)
        path = save_rows(rows, day, station)
        print(f"{day} {station}: {len(rows)} rows -> {path}")


    
if __name__=="__main__":
    main()