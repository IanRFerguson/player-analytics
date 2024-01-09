from prefect import flow
from parsons.google.google_bigquery import GoogleBigQuery
from parsons import Table
import datetime
from src.utils import scrape_basketball_reference, clean_player_data

#####


def get_data_from_source():
    """
    Scrapes and cleans NYK player data
    """

    date_yesterday = datetime.date.today() - datetime.timedelta(days=1)
    player_data = scrape_basketball_reference(target=date_yesterday)

    if player_data:
        player_data = clean_player_data(player_data=player_data)
        return player_data


def load_data_to_warehouse(bq: GoogleBigQuery, nyk_data: Table):
    """
    Loads cleaned data into BigQuery
    """

    pass


@flow(log_prints=True)
def run(bq: GoogleBigQuery):
    nyk_data = get_data_from_source()

    if nyk_data:
        load_data_to_warehouse(bq=bq, nyk_data=nyk_data)


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
