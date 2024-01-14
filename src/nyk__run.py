from prefect import flow
from parsons.google.google_bigquery import GoogleBigQuery
import datetime
from src.api import get_all_boxscore_data
from src.utilities.cli import cli
from src.utilities.logger import logger
import os

#####


@flow(log_prints=True)
def run(bq: GoogleBigQuery, full_refresh: bool):
    # Get formatted date from yesterday
    today_ = datetime.date.today()
    yesterday_ = (today_ - datetime.timedelta(days=1)).strftime("%b %d, %Y").upper()

    get_all_boxscore_data(bq=bq, full_refresh=full_refresh, target=yesterday_)


#####

if __name__ == "__main__":
    # Instantiate connection to BigQuery
    bq = GoogleBigQuery(app_creds=os.environ["GCP_CREDS"])

    args_ = cli()

    if args_.debug:
        logger.setLevel(level=10)
        logger.debug("Running in debug mode...")

    # Serve Prefect workflow
    run.serve(
        name="nyk-player-data",
        tags=["onboarding"],
        parameters={"bq": bq, "full_refresh": args_.full_refresh},
        interval=60,
    )
