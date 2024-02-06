import os
import subprocess
from utilities.bigquery import BigQuery
from utilities.logger import logger
from utilities.json_helpers import load_config

##########

# FIXME - This still isn't working
def authenticate(api_key: str, workspace: str):
    """
    WIP - Runs `prefect cloud login` command to authenticate program
    """
    call_ = (f"prefect cloud login --key {api_key} --workspace {workspace}").split(" ")
    subprocess.Popen(call_).wait()


def deploy():
    """
    Kicks off Prefect Cloud deployment
    """

    call_ = "prefect deployment run nba-player-analytics/nyk-player-data".split(" ")
    subprocess.Popen(call_).wait()


#####

if __name__ == "__main__":
    # Pull in local config object
    config_ = load_config()

    # Login to Prefect Cloud
    key_ = config_.pop("PREFECT_API_KEY").replace('"', "")
    workspace_ = config_.pop("PREFECT_WORKSPACE").replace('"', "")
    authenticate(api_key=key_, workspace=workspace_)
