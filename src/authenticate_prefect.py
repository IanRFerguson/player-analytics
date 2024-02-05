import os
import subprocess
from pull_config_into_environment import main as setup_config
from utilities.bigquery import BigQuery
from utilities.logger import logger

##########

# FIXME - This still isn't working
def main(api_key: str, workspace: str):
    """
    WIP - Runs `prefect cloud login` command to authenticate program
    """
    call_ = (f"prefect cloud login --key {api_key} --workspace {workspace}").split(" ")
    subprocess.run(call_)


#####

if __name__ == "__main__":
    # TODO - Make this abstract
    service_creds = "./service_accounts/nba-player-analytics-4153526c6e83.json"
    if not os.environ.get("GCP_CREDS"):
        logger.info("Manually setting environment var...")
        os.environ["GCP_CREDS"] = service_creds

    # Instantiate BigQuery client
    bq = BigQuery(service_credentials=os.environ["GCP_CREDS"])

    # Set environment from BigQuery config
    setup_config(bq=bq)

    # Login to Prefect Cloud
    main()
