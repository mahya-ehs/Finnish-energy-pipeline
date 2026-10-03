from pathlib import Path
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets

import time
from datetime import date, timedelta
import dagster as dg
from ingestion import fingrid, entsoe, fmi
from transforms import parser_entsoe, parse_fmi

DBT_PROJECT_DIR = Path(__file__).resolve().parent.parent / "energy_dbt"
dbt_project = DbtProject(
    project_dir=DBT_PROJECT_DIR,
    profiles_dir=Path.home() / ".dbt",
)
dbt_project.prepare_if_dev()

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

@dbt_assets(manifest=dbt_project.manifest_path)
def energy_dbt_assets(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
    
        
defs = dg.Definitions(
    assets=[
        raw_fingrid_consumption,
        raw_entsoe_prices,
        raw_fmi_weather,
        staging_entsoe_prices,
        staging_fmi_weather,
        energy_dbt_assets,
    ],
    resources={"dbt": DbtCliResource(project_dir=dbt_project)},
)