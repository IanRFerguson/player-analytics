import os
from pull_config_into_environment import main as setup_config
from authenticate_prefect import main as authenticate
from run__local import kickoff
from utilities.bigquery import BigQuery
from utilities.logger import logger
from utilities.json_helpers import load_config
from config import TEAM_CONFIG

##########


def main(bq: BigQuery, refresh: bool = False, testing: bool = False):

    # Pull config from BigQuery to local environment
    setup_config(bq=bq, save_locally=True)
    local_config = load_config()
    team_prefix = local_config["TEAM_ABBREVIATION"].replace('"', "")

    # Authenticate with Prefect Cloud
    authenticate(
        api_key=local_config["PREFECT_API_KEY"].replace('"', ""),
        workspace=local_config["PREFECT_WORKSPACE"].replace('"', ""),
    )

    # Serve Prefect workflow
    kickoff.serve(
        name="nyk-player-data",
        tags=["analytics"],
        parameters={
            "full_refresh": refresh,
            "dataset": TEAM_CONFIG[team_prefix]["dataset"],
            "team_id": TEAM_CONFIG[team_prefix]["id"],
            "testing": testing,
            "team_abbreviation": team_prefix,
        },
        cron="0 11 * * *",
    )


#####

if __name__ == "__main__":
    # TODO - Make this abstract
    service_creds = "./service_accounts/nba-player-analytics-4153526c6e83.json"
    if not os.environ.get("GCP_CREDS"):
        logger.info("Manually setting environment var...")
        os.environ["GCP_CREDS"] = service_creds

    # Instantiate BigQuery client
    bq = BigQuery(service_credentials=os.environ["GCP_CREDS"])
    main(bq=bq)
