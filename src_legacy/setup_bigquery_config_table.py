import os
import datetime
import json
from dotenv import load_dotenv
import pandas as pd
from utilities.bigquery import BigQuery

##########


def infer_dev_environment(file_path: str = "../development.env"):
    """
    Loads local environment file when there is an environment mismatch
    """

    check_for_local_file(file_path=file_path)

    if not os.environ.get("GCP_CREDS"):
        load_dotenv(file_path)


def check_for_local_file(file_path: str = "../development.env"):
    """
    Ensures that local environment file is present
    """

    if not os.path.exists(file_path):
        raise OSError(f"{file_path} not found")


def get_absolute_path_to_env():
    """
    Cleans up absolute path to environment file
    """

    current_dir = os.path.dirname(__file__)
    relative_path = os.path.join(current_dir, "..", "development.env")

    return os.path.abspath(relative_path)


def get_dictionary_from_env_file(file_path: str = "../development.env"):
    """
    Creates dictionary representation of local
    environment file
    """
    check_for_local_file(file_path=file_path)

    with open(file_path) as temp_:
        base_ = temp_.read()

    # Filestream -> list
    base_ = [x.split("=") for x in base_.split("\n")]

    # List -> dictionary
    base_ = {k: v for [k, v] in base_}

    return base_


def build_dataframe_from_env_file(file_path: str = "../development.env"):
    """
    Creates a Pandas DataFrame from local environment file
    """

    env_dictionary = get_dictionary_from_env_file(file_path=file_path)
    timestamp_ = datetime.datetime.now()

    df = pd.DataFrame(
        {"config_timestamp": timestamp_, "config": json.dumps(env_dictionary)},
        index=[0],
    )

    return df


def write_config_dataframe_to_bigquery(
    bq: BigQuery, df: pd.DataFrame, config_table_name: str
):
    bq.copy_dataframe_to_bigquery(
        dataframe=df, table_name=config_table_name, if_exists="append"
    )


def setup_config_table(bq: BigQuery, config_table_name: str):
    """
    Creates the destination config table if it doesn't exist
    """

    create_sql = f"""
    CREATE TABLE {config_table_name} (
        config_timestamp TIMESTAMP,
        config STRING
    );
    """

    bq.query(sql=create_sql, return_result=False)


def main(bq: BigQuery, config_table_name: str, path_to_local_env: str):
    # Determine if the config table exists
    if not bq.table_exists(table_name=config_table_name):
        setup_config_table(bq=bq, config_table_name=config_table_name)

    # Write a Pandas DataFrame to BigQuery representing local environment
    config_dataframe = build_dataframe_from_env_file(file_path=path_to_local_env)
    write_config_dataframe_to_bigquery(
        bq=bq, df=config_dataframe, config_table_name=config_table_name
    )


#####

if __name__ == "__main__":
    # Find local development.env file
    file_path = get_absolute_path_to_env()

    # Sets environment when necessary
    infer_dev_environment(file_path=file_path)

    # Instantiate BigQuery client
    bq = BigQuery(service_credentials=os.environ["GCP_CREDS"])

    # Write config table to BigQuery
    main(bq=bq, config_table_name="config.load_config", path_to_local_env=file_path)
