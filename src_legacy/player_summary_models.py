import os
from utilities.logger import logger
from utilities.bigquery import BigQuery

##########


def get_player_names_from_bigquery(
    bq: BigQuery, table: str = "dbt_staging.stg_player__lookup"
):
    query_ = f"SELECT id, name FROM {table}"
    result_ = bq.query(query_)

    return result_


def create_summary_model_file(path_to_dbt_subdirectory: str, result_set):
    for ix in result_set.index:
        model_name = result_set["name"][ix].replace(".", "").replace(" ", "_").lower()
        file_name = os.path.join(path_to_dbt_subdirectory, f"summary__{model_name}.sql")

        if not os.path.exists(file_name):
            logger.info(
                f"Creating new model for {result_set['name'][ix]} [player_id={result_set['id'][ix]}]"
            )

            with open(file_name, "w") as temp_:
                build_cmd = "build_player_summary_models(player_id='{}')".format(
                    result_set["id"][ix]
                )
                temp_.write("{{ " + build_cmd + " }}")


def sync_player_summary_models(
    bq: BigQuery,
    path_to_dbt_subdirectory: str,
    table: str = "nba_dbt__staging.stg_player__lookup",
):
    all_player_names = get_player_names_from_bigquery(bq=bq, table=table)
    create_summary_model_file(
        path_to_dbt_subdirectory=path_to_dbt_subdirectory, result_set=all_player_names
    )


#####

if __name__ == "__main__":
    bq = BigQuery(service_credentials=os.environ["GCP_CREDS"])
    here_ = os.path.dirname(__file__)
    player_summary_path = os.path.join(here_, "../nba_dbt/models/player_summaries")

    sync_player_summary_models(bq=bq, path_to_dbt_subdirectory=player_summary_path)
