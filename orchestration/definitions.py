import time
from datetime import date, timedelta
import dagster as dg
from ingestion import fingrid, entsoe, fmi
from transforms import parser_entsoe, parse_fmi

@dg.asset
def raw_fingrid_consumption():
    day = date.today() - timedelta(days=1)
    fingrid.ingest_day(day)


@dg.asset
def raw_entsoe_prices():
    day = date.today() - timedelta(days=1)
    res = entsoe.fetch_day(day)
    entsoe.save_raw(res, day)

@dg.asset(deps=["raw_entsoe_prices"])
def staging_entsoe_prices():
    parser_entsoe.main()
    
@dg.asset
def raw_fmi_weather():
    day = date.today() - timedelta(days=1)
    for station, fmisid in fmi.STATIONS.items():
        res = fmi.fetch_day(fmisid, day)
        fmi.save_raw(res, day, station)
        time.sleep(1)

@dg.asset(deps=["raw_fmi_weather"])
def staging_fmi_weather():
    parse_fmi.main()
    
defs = dg.Definitions(
    assets=[
        raw_fingrid_consumption,
        raw_entsoe_prices,
        raw_fmi_weather,
        staging_entsoe_prices,
        staging_fmi_weather,
    ]
)