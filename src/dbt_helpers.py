import os
import subprocess
from utilities.logger import logger

#####


def set_dbt_path():
    here_ = os.path.dirname(__file__)
    dbt_path = os.path.join(here_, "../nba_dbt")
    os.chdir(dbt_path)


def dbt_models(target: str = "+path:models/staging"):
    call_ = f"dbt build --select {target}".split(" ")
    logger.debug(f"Attempting to run dbt from {os.getcwd()}")
    logger.debug(f"Call: {call_}")
    subprocess.run(call_)


def dbt_deps():
    call_ = "dbt deps".split(" ")
    logger.debug("Running dbt deps...")
    logger.debug(f"Call: {call_}")
    subprocess.run(call_)


def build_dbt(target: str = "+path:models/staging"):
    set_dbt_path()
    dbt_deps()
    dbt_models(target=target)


if __name__ == "__main__":
    logger.setLevel(level=10)
    build_dbt()
