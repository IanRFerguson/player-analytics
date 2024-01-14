import os
from parsons.google.google_bigquery import GoogleBigQuery
import datetime
from api import get_all_boxscore_data
from utilities.cli import cli
from utilities.logger import logger
from config import RAW_BQ_DATASET

#####


def run(bq: GoogleBigQuery, full_refresh: bool):
    # Get formatted date from yesterday
    today_ = datetime.date.today()
    yesterday_ = (today_ - datetime.timedelta(days=1)).strftime("%b %d, %Y").upper()

    test_dataset = f"{RAW_BQ_DATASET}__test"

    get_all_boxscore_data(
        bq=bq, full_refresh=full_refresh, target=yesterday_, dataset=test_dataset
    )


#####

if __name__ == "__main__":
    # Instantiate connection to BigQuery
    bq = GoogleBigQuery(app_creds=os.environ["GCP_CREDS"])

    args_ = cli()

    if args_.debug:
        logger.setLevel(level=10)
        logger.debug("Running in debug mode...")

    run(bq=bq, full_refresh=args_.full_refresh)
