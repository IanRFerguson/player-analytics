from prefect import flow
from parsons.google.google_bigquery import GoogleBigQuery
from parsons import Table
import datetime
from src.utils import get_all_boxscore_data

#####


def load_data_to_warehouse(bq: GoogleBigQuery, nyk_data: Table):
    """
    Loads cleaned data into BigQuery
    """

    pass


@flow(log_prints=True)
def run(bq: GoogleBigQuery):
    pass


#####

if __name__ == "__main__":
    # Instantiate connection to BigQuery
    bq = GoogleBigQuery()

    # Serve Prefect workflow
    run.serve(
        name="nyk-player-data",
        tags=["onboarding"],
        parameters={"bq": bq},
        interval=60,
    )
