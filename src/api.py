import json
import pandas as pd
from parsons import Table
from parsons.google.google_bigquery import GoogleBigQuery
from nba_api.stats.endpoints.teamgamelog import TeamGameLog
from config import RAW_BQ_DATASET, STAT_TABLE_CONFIG, TEAM_ID
from utilities.logger import logger

#####

logger.info("Hello world")


def get_game_metadata(team_id: str = TEAM_ID):
    """
    Hits the NBA API and returns dataframe of all games that
    have already been played this season
    """

    # Get all previous games
    games_ = json.loads(TeamGameLog(1610612752).get_json())["resultSets"][0]

    # Shape into tabular data
    data_ = pd.DataFrame(games_["rowSet"], columns=games_["headers"])

    return data_


def get_all_boxscore_data(target: str, bq: GoogleBigQuery, full_refresh: bool = False):
    """
    Retrives player data for a given date. If the Knicks
    did not play a game on this date, the function
    returns `None`
    """

    all_game_metadata = get_game_metadata()

    if not full_refresh:
        all_game_metadata = all_game_metadata[
            all_game_metadata["GAME_DATE"] == target
        ].reset_index(drop=True)

        if not len(all_game_metadata) == 1:
            return None

    game_ids = [x for x in all_game_metadata["Game_ID"]]

    all_errors = []
    for ix, id_ in enumerate(game_ids):
        process(
            index=ix,
            id_=id_,
            bq=bq,
            full_refresh=full_refresh,
            error_manifest=all_errors,
        )

    if all_errors:
        logger.error(f"{len(all_errors)} builds failed")

        for e in all_errors:
            logger.error(e)

        raise


def build_tables(
    data: pd.DataFrame,
    raw_table_name: str,
    raw_dataset: str,
    bq: GoogleBigQuery,
):
    # Full dataset.table name
    table_name = f"{raw_dataset}.{raw_table_name}"

    # Convert DataFrame to Parsons table
    # TODO: Should be easy to clean this up
    tbl = Table().from_dataframe(dataframe=data)

    # Copy data to BigQuery
    bq.copy(tbl=tbl, table_name=table_name, if_exists="append")


def process(
    index: int, id_: str, bq: GoogleBigQuery, full_refresh: bool, error_manifest: list
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

        # Drop the table if desired (but only in the first loop)
        if full_refresh and index == 0:
            logger.debug(f"Attempting to drop table {raw_table_name}...")
            bq.delete_table(table_name=f"{RAW_BQ_DATASET}.{raw_table_name}")
            logger.info(f"Successfully dropped table {RAW_BQ_DATASET}.{raw_table_name}")

        try:
            # Use API to build dataframe
            data = endpoint(id_).get_data_frames()[0]
            data = data[data[team_id_field] == TEAM_ID].reset_index(drop=True)
            logger.debug("Successfully built dataframes")

            # Write data to BigQuery
            build_tables(
                data=data,
                raw_dataset=RAW_BQ_DATASET,
                raw_table_name=raw_table_name,
                full_refresh=full_refresh,
            )
            logger.debug("Successfully wrote to BigQuery")

        except Exception as e:
            logger.error(f"Build type {build_type} failed for id={id_}")
            logger.error(e)
            error_manifest.append({"id": id_, "type": build_type})
