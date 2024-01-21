import json
import datetime
import pandas as pd
from utilities.bigquery import BigQuery
from nba_api.stats.endpoints.teamgamelog import TeamGameLog
from config import RAW_BQ_DATASET, STAT_TABLE_CONFIG, NYK_ID, LOG_TABLE
from utilities.logger import logger

#####


def get_game_metadata(team_id: str = NYK_ID):
    """`
    Hits the NBA API and returns dataframe of all games that
    have already been played this season
    """

    # Get all previous games
    games_ = json.loads(TeamGameLog(team_id).get_json())["resultSets"][0]
    logger.debug("Successfully queried team game log...")

    # Shape into tabular data
    data_ = pd.DataFrame(games_["rowSet"], columns=games_["headers"])
    logger.debug("Cast game data to table...")

    return data_


def get_all_boxscore_data(
    bq: BigQuery,
    full_refresh: bool = False,
    dataset: str = RAW_BQ_DATASET,
):
    """
    Retrives player data for a given date. If the Knicks
    did not play a game on this date, the function
    returns `None`
    """

    log_table = f"{dataset}.{LOG_TABLE}"
    all_game_metadata = get_game_metadata()
    build_tables(
        data=all_game_metadata,
        raw_dataset=dataset,
        raw_table_name="game_log",
        if_exists="drop",
        bq=bq,
    )

    if full_refresh and bq.table_exists(table_name=log_table):
        # Truncate the log table to start fresh
        bq.drop_table(table_name=log_table)
        drop_destination_tables(
            bq=bq,
            dataset=dataset,
            destination_tables=[
                STAT_TABLE_CONFIG[x]["raw_table_name"] for x in STAT_TABLE_CONFIG.keys()
            ],
        )

    ###

    all_errors = []
    existing_game_ids = get_ids_from_log_table(
        log_table=log_table, game_log_table=f"{dataset}.game_log", bq=bq
    )
    game_ids = [x for x in all_game_metadata["Game_ID"] if x not in existing_game_ids]

    if len(game_ids) == 0:
        logger.info("No new games to log")
        return

    logger.debug(f"Identified {len(game_ids)} Game IDs to process...")
    logger.info(f"Processing {len(game_ids)} games...")

    for id_ in game_ids:
        process(
            id_=id_,
            bq=bq,
            error_manifest=all_errors,
            dataset=dataset,
            log_table=log_table,
        )

    if all_errors:
        logger.error(f"{len(all_errors)} builds failed")
        for e in all_errors:
            logger.error(e)
        raise

    logger.info(f"{len(game_ids)} games processed successfully")
    return True


def build_tables(
    data: pd.DataFrame,
    raw_table_name: str,
    raw_dataset: str,
    bq: BigQuery,
    if_exists: str = "append",
):
    # Full dataset.table name
    table_name = f"{raw_dataset}.{raw_table_name}"
    logger.debug(f"Processing {raw_dataset}.{raw_table_name}...")

    bq.copy_dataframe_to_bigquery(
        dataframe=data, table_name=table_name, if_exists=if_exists
    )


def process(
    id_: str,
    bq: BigQuery,
    error_manifest: list,
    log_table: str,
    dataset: str = RAW_BQ_DATASET,
):
    """
    Iteratively hits stat-specific API endpoints and writes the responses
    to BigQuery tables
    """

    logger.info(f"Processing id={id_}")

    # Loop through different analytics tables
    for build_type in STAT_TABLE_CONFIG:
        # Get metadata from config
        endpoint = STAT_TABLE_CONFIG[build_type]["api_endpoint"]
        raw_table_name = STAT_TABLE_CONFIG[build_type]["raw_table_name"]
        team_id_field = STAT_TABLE_CONFIG[build_type]["team_id_field"]
        ignore_columns = STAT_TABLE_CONFIG[build_type]["ignore_columns"]

        try:
            # Use API to build dataframe
            data = endpoint(id_).get_data_frames()[0]
            data = data[data[team_id_field].astype(str) == NYK_ID].reset_index(
                drop=True
            )

            if ignore_columns:
                logger.debug(f"Dropping the following columns: {ignore_columns}")
                data = data.drop(ignore_columns, axis=1)

            logger.debug("Successfully built dataframes")

        except Exception as e:
            logger.error(f"Build type {build_type} failed for id={id_} at DATA STAGE")
            logger.error(e)
            error_manifest.append({"game_id": id_, "type": build_type, "stage": "data"})

        ###

        try:
            # Write data to BigQuery
            build_tables(
                data=data, raw_dataset=dataset, raw_table_name=raw_table_name, bq=bq
            )
            logger.debug("Successfully wrote to BigQuery")

        except Exception as e:
            logger.error(f"Build type {build_type} failed for id={id_} at BUILD STAGE")
            logger.error(e)
            error_manifest.append(
                {"game_id": id_, "type": build_type, "stage": "build"}
            )

    write_to_log_table(log_table=log_table, game_id=id_, bq=bq)


def write_to_log_table(log_table: str, game_id: str, bq: BigQuery):
    """
    Writes ELT metadata to log table
    """

    meta_ = pd.DataFrame([{"id": game_id, "_load_timestamp": datetime.datetime.now()}])
    bq.copy_dataframe_to_bigquery(
        dataframe=meta_, table_name=log_table, if_exists="append"
    )


def get_ids_from_log_table(log_table: str, game_log_table: str, bq: BigQuery) -> list:
    """
    Queries all LOGGED and INCOMPLETE games. We don't want to attempt
    to write API results for ongoing games as the data types get
    misconfigured
    """

    logger.debug(f"Checking ids against {log_table}...")

    # We assume that this table exists ... the API nullifies
    # many fields if a game is actively in progress, which is
    # maybe helpful but not for our purposes
    incomplete_games_query = (
        f"SELECT DISTINCT GAME_ID AS id_ FROM {game_log_table} WHERE WL IS NULL"
    )
    incomplete_games = [x for x in bq.query(incomplete_games_query)["id_"]]

    if bq.table_exists(table_name=log_table):
        query = f"SELECT DISTINCT id FROM {log_table}"
        result = bq.query(query, return_values=True)

        return set([x for x in result["id"]] + incomplete_games)

    logger.debug(f"{log_table} doesn't exist, returning incomplete games only...")
    return incomplete_games


def drop_destination_tables(destination_tables: list, bq: BigQuery, dataset: str):
    """
    Iteratively drops destination tables when FULL_REFRESH
    is set to True
    """

    for table_ in destination_tables:
        logger.debug(f"Dropping {table_}...")
        bq.drop_table(table_name=f"{dataset}.{table_}")
