import os
import logging
from prefect import flow, task, get_run_logger
from api_helpers import get_all_boxscore_data
from dbt_helpers import build_dbt
from utilities.cli import cli
from utilities.logger import logger
from utilities.environment import set_dataset, set_environment
from utilities.bigquery import BigQuery
from pull_config_into_environment import main as setup_config

#####


@flow(name="nba-player-analytics", log_prints=True)
def kickoff(
    full_refresh: bool, dataset: str, testing: bool, team_abbrevation: str, team_id: str
):
    bq = BigQuery(service_credentials=os.environ["GCP_CREDS"])
    successful_run = run_api(
        bq=bq,
        full_refresh=full_refresh,
        dataset=dataset,
        team_abbrevation=team_abbrevation,
        team_id=team_id,
    )

    if successful_run and not testing:
        run_dbt()


@task
def run_api(
    bq: BigQuery, full_refresh: bool, dataset: str, team_abbrevation: str, team_id: str
):
    return get_all_boxscore_data(
        bq=bq,
        full_refresh=full_refresh,
        dataset=dataset,
        team_abbrevation=team_abbrevation,
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
    DATASET = set_dataset(TESTING)

    if DEBUG:
        logger.setLevel(level=10)
        logger.debug("Running logger in debug...")

    logger.info("Running with the following config...")
    config = {
        "Local Run": LOCAL,
        "Full Refresh": FULL_REFRESH,
        "Testing": TESTING,
        "Destination Dataset": DATASET,
    }

    ###

    if LOCAL:
        bq = BigQuery(service_credentials=os.environ["GCP_CREDS"])
        run_api.fn(bq=bq, full_refresh=FULL_REFRESH, dataset=DATASET)
        run_dbt.fn()

    else:
        setup_config(variables=["TEAM_ABBREVIATION"])
        kickoff.serve(
            name="nyk-player-data",
            tags=["analytics"],
            parameters={
                "full_refresh": FULL_REFRESH,
                "dataset": DATASET,
                "testing": TESTING,
                "team_abbreviation": "nyk",
            },
            cron="0 11 * * *",
        )