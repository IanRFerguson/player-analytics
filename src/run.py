import os
from prefect import flow, task
from api_helpers import get_all_boxscore_data
from dbt_helpers import build_dbt
from utilities.cli import cli
from utilities.logger import logger
from utilities.environment import set_dataset, set_environment
from utilities.bigquery import BigQuery

##########


@flow(name="nba-player-analytics")
def kickoff(
    full_refresh: bool, dataset: str, testing: bool, team_id: str
):
    bq = BigQuery(service_credentials=os.environ["GCP_CREDS"])
    successful_run = run_api(
        bq=bq,
        full_refresh=full_refresh,
        dataset=dataset,
        team_id=team_id,
    )

    if successful_run and not testing:
        run_dbt()


@task
def run_api(
    bq: BigQuery, full_refresh: bool, dataset: str, team_id: str
):
    return get_all_boxscore_data(
        bq=bq,
        full_refresh=full_refresh,
        dataset=dataset,
        team_id=team_id,
    )


@task
def run_dbt():
    build_dbt()


#####

if __name__ == "__main__":
    set_environment()
    args_ = cli()

    # Parse
    LOCAL = args_.local
    FULL_REFRESH = args_.full_refresh
    TESTING = args_.test
    DEBUG = args_.debug
    DATASET = set_dataset(TESTING, default_dataset="raw__nyk_data")

    if DEBUG:
        logger.setLevel(level=10)
        logger.debug("Running logger in debug...")

    ###

    if LOCAL:
        logger.debug(os.environ["GCP_CREDS"])
        bq = BigQuery(service_credentials=os.environ["GCP_CREDS"])
        run_api.fn(
            bq=bq,
            full_refresh=FULL_REFRESH,
            dataset=DATASET,
            team_id="1610612752",
        )
        run_dbt.fn()

    else:
        kickoff.serve(
            name="nyk-player-data",
            tags=["analytics"],
            parameters={
                "full_refresh": FULL_REFRESH,
                "dataset": DATASET,
                "testing": TESTING,
                "team_id": "1610612752",
            },
            # cron="0 16 * * *",
            interval=80,
        )
