from dotenv import load_dotenv
import os
from utilities.logger import logger

#####


def set_dataset(testing: bool, default_dataset: str):
    """
    Adds test flag to BigQuery dataset name if applicable
    """

    if testing:
        return f"{default_dataset}__test"

    return default_dataset


def set_environment():
    """
    Loads environment variables to work across mutliple
    deployment environments
    """

    here_ = os.path.dirname(__file__)
    env_path = os.path.abspath(os.path.join(here_, "../../development.env"))
    load_dotenv(dotenv_path=env_path)


if __name__ == "__main__":
    logger.setLevel(level=10)
    set_environment()
