import os
import logging
from prefect import flow, task
from parsons.google.google_bigquery import GoogleBigQuery
from api_helpers import get_all_boxscore_data
from dbt_helpers import build_dbt
from utilities.cli import cli
from utilities.logger import logger
from config import RAW_BQ_DATASET

#####


def set_dataset(testing: bool):
    if testing:
        return f"{RAW_BQ_DATASET}__test"

    return RAW_BQ_DATASET


@flow(log_prints=False)
def kickoff(full_refresh: bool, dataset: str, testing: bool):
    bq = GoogleBigQuery(app_creds=os.environ["GCP_CREDS"])
    successful_run = run_api(bq=bq, full_refresh=full_refresh, dataset=dataset)

    if successful_run and not testing:
        run_dbt()


@task
def run_api(bq: GoogleBigQuery, full_refresh: bool, dataset: str = RAW_BQ_DATASET):
    return get_all_boxscore_data(bq=bq, full_refresh=full_refresh, dataset=dataset)


@task
def run_dbt():
    build_dbt()


#####

if __name__ == "__main__":
    # Get command line args
    args_ = cli()

    # Parse
    LOCAL = args_.local
    FULL_REFRESH = args_.full_refresh
    TESTING = args_.test
    DEBUG = args_.debug
    DATASET = set_dataset(TESTING)

    if DEBUG:
        logger.setLevel(level=10)
        logger.debug("Running logger in debug...")
    else:
        # If we're running the logger normally we don't really need all
        # the logs we get from Parsons
        logging.getLogger("parsons.google.google_cloud_storage").setLevel(level=30)

    ###

    logger.info("Running with the following config...")
    config = {
        "Local Run": LOCAL,
        "Full Refresh": FULL_REFRESH,
        "Testing": TESTING,
        "Destination Dataset": DATASET,
    }
    for key in config.keys():
        logger.info(f"{key.upper()}:\t{config[key]}")

    ###

    if LOCAL:
        bq = GoogleBigQuery(app_creds=os.environ["GCP_CREDS"])
        run_api.fn(bq=bq, full_refresh=FULL_REFRESH, dataset=DATASET)
        run_dbt.fn()

    else:
        kickoff.serve(
            name="nyk-player-data",
            tags=["analytics"],
            parameters={
                "full_refresh": FULL_REFRESH,
                "dataset": DATASET,
                "testing": TESTING,
            },
            interval=6000,
        )
