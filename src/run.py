import os
import datetime
import logging
import pytz
from prefect import flow, task
from parsons.google.google_bigquery import GoogleBigQuery
from api import get_all_boxscore_data
from utilities.cli import cli
from utilities.logger import logger
from config import RAW_BQ_DATASET

#####


def generate_target():
    """
    Creates formatted datetime string representing yesterday's date
    """

    # Get formatted date from yesterday
    today_ = datetime.datetime.now(tz=pytz.timezone("US/Eastern"))

    # Format date string
    yesterday_ = (today_ - datetime.timedelta(days=1)).strftime("%b %d, %Y").upper()

    return yesterday_


def set_dataset(testing: bool):
    if testing:
        return f"{RAW_BQ_DATASET}__test"

    return RAW_BQ_DATASET


@flow(log_prints=True)
def kickoff(full_refresh: bool, dataset: str):
    bq = GoogleBigQuery(app_creds=os.environ["GCP_CREDS"])
    run(bq=bq, full_refresh=full_refresh, dataset=dataset)


@task
def run(bq: GoogleBigQuery, full_refresh: bool, dataset: str = RAW_BQ_DATASET):
    target = generate_target()

    get_all_boxscore_data(
        bq=bq, full_refresh=full_refresh, target=target, dataset=dataset
    )


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
    logger.info(config)

    ###

    if LOCAL:
        bq = GoogleBigQuery(app_creds=os.environ["GCP_CREDS"])
        run.fn(bq=bq, full_refresh=FULL_REFRESH, dataset=DATASET)

    else:
        kickoff.serve(
            name="nyk-player-data",
            tags=["analytics"],
            parameters={"full_refresh": FULL_REFRESH, "dataset": DATASET},
            interval=60,
        )
