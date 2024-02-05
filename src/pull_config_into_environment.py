import json
import os
from utilities.logger import logger
from utilities.bigquery import BigQuery
from utilities.json_helpers import save_config

##########


def get_config_dictionary_from_bigquery(bq: BigQuery):
    """
    Returns the latest config dictionary from BigQuery config table
    """

    config_sql = """
    SELECT 
        config 
    FROM config.load_config 
    ORDER BY config_timestamp DESC
    LIMIT 1
    """

    config_ = bq.query(sql=config_sql)["config"][0]

    return json.loads(config_)


def main(bq: BigQuery, variables: list = [], save_locally: bool = False):
    config_ = get_config_dictionary_from_bigquery(bq=bq)

    if not variables:
        variables = [x for x in config_.keys()]

    if save_locally:
        logger.info("Saving JSON configuration locally...")
        save_config(config_object=config_)

    else:
        for key_ in variables:
            logger.info(f"Setting {key_}...")
            os.environ[key_] = config_[key_]


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
