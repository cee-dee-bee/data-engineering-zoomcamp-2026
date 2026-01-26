#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
import click

gtt_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet'
zones_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv'

gtt_df = pd.read_parquet(gtt_url)

zones_df= pd.read_csv(zones_url)

@click.command()
@click.option('--pg-user', envvar="PG_USER", default="root", help="postgres user")
@click.option('--pg-pass', envvar="PG_PASS", default="root")
@click.option('--pg-host', envvar="PG_HOST", default="localhost")
@click.option('--pg-port', envvar="PG_PORT", default=5432)
@click.option('--pg-db', envvar="PG_DB", default="ny_taxi_hw")
def ingest(pg_user, pg_pass, pg_host, pg_port, pg_db):
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    print("creating tables..")
    gtt_df.head(0).to_sql(
        name="green_taxi_trips",
        con=engine,
        if_exists="replace"
    )
    print("green taxi data table created")

    zones_df.head(0).to_sql(
        name="zones",
        con=engine,
        if_exists="replace"
    )
    print("zones tables created")

    print("ingesting data..")
    gtt_df.to_sql(
        name="green_taxi_trips",
        con=engine,
        if_exists="append"
    )
    print("done ingesting data for green taxi trips table")
    print(f"{len(gtt_df)} rows inserted")
    zones_df.to_sql(
        name="zones",
        con=engine,
        if_exists="append"
    )
    print("done ingesting data for zones table")
    print(f"{len(zones_df)} rows inserted")

if __name__ == '__main__':
    ingest()