import xml.etree.ElementTree as ET
import requests

NS = {"BsWfs": "http://xml.fmi.fi/schema/wfs/2.0"}
URL = "https://opendata.fmi.fi/wfs"
BASE = {
    "service": "WFS", "version": "2.0.0", "request": "getFeature",
    "fmisid": 101786,  # Oulu airport
    "starttime": "2026-09-28T00:00:00Z", "endtime": "2026-09-28T02:00:00Z",
}

def get(params):
    root = ET.fromstring(requests.get(URL, params={**BASE, **params}, timeout=30).content)
    return [(e.find("BsWfs:Time", NS).text,
             e.find("BsWfs:ParameterName", NS).text,
             e.find("BsWfs:ParameterValue", NS).text)
            for e in root.findall(".//BsWfs:BsWfsElement", NS)]

print("10-minute temperatures:")
for t, p, v in get({"storedquery_id": "fmi::observations::weather::simple",
                    "parameters": "t2m", "timestep": 10}):
    print(" ", t, v)

print("Hourly averages:")
for t, p, v in get({"storedquery_id": "fmi::observations::weather::hourly::simple",
                    "parameters": "TA_PT1H_AVG"}):
    print(" ", t, v)