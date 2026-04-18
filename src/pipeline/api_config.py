import backoff
import dlt
import requests as http_client
from constants import RuntimeConfig
from google.cloud import bigquery
from pydantic import BaseModel
from requests.exceptions import HTTPError

from common.logger import pipeline_logger

#####

BIGQUERY_CLIENT = bigquery.Client()


@backoff.on_exception(
    backoff.expo,
    HTTPError,
    max_tries=20,
    base=10,
    on_backoff=lambda details: pipeline_logger.warning(
        f"Request failed with error: {details['exception']}. Backing off for {details['wait']} seconds..."
    ),
    giveup=lambda e: e.response is not None and e.response.status_code != 429,
)
def _fetch_page(url: str, headers: dict, params: dict | list) -> dict:
    """
    Helper function to fetch a single page of results from the API with backoff on failure.

    Args:
        url (str): The API endpoint URL to fetch data from.
        headers (dict): The HTTP headers to include in the request, such as authentication tokens.
        params (dict | list): The query parameters to include in the request, which can be either a dictionary or a list of tuples for multiple values with the same key.

    Returns:
        dict: The JSON response from the API.

    Raises:
        HTTPError: If the request fails with an HTTP error status code.
    """
    response = http_client.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def _fetch_all_games(
    base_url: str, headers: dict, team_id: int, start_date: str | None = None
) -> list[dict]:
    """
    Paginate through all games and return the full list of game objects.

    Args:
        base_url (str): The base URL of the API.
        headers (dict): The HTTP headers to include in the request, such as authentication tokens.
        team_id (int): The ID of the team to fetch games for.
        start_date (str | None): The starting date for filtering games. If None, all games will be fetched.

    Returns:
        list[dict]: A list of game objects.
    """

    games: list[dict] = []
    cursor = None
    while True:
        params: dict = {"team_ids[]": team_id, "per_page": 100}
        if start_date:
            params["start_date"] = start_date
        if cursor:
            params["cursor"] = cursor
        body = _fetch_page(f"{base_url}/v1/games", headers, params)
        games.extend(body["data"])
        cursor = body.get("meta", {}).get("next_cursor")
        if not cursor:
            break
    return games


def _chunks(lst: list, size: int):
    """
    Yield successive fixed-size chunks from a list.

    Args:
        lst (list): The list to be divided into chunks.
        size (int): The size of each chunk.

    Yields:
        list: A chunk of the original list.
    """
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


def get_latest_record(destination_schema: str) -> str | None:
    """
    Query the destination for the latest record date in the games table to determine the starting point for incremental loading.

    Args:
        destination_schema (str): The schema in the destination where the data is stored.

    Returns:
        str | None: The latest record date as a string in ISO format, or None if no records are found.
    """

    query = f"""
        SELECT MAX(date) AS latest_date
        FROM `{destination_schema}.games`
    """

    query_job = BIGQUERY_CLIENT.query(query)
    result = query_job.result()
    latest_date = None
    for row in result:
        latest_date = row["latest_date"]

    if latest_date:
        pipeline_logger.info(f"Latest record date in destination: {latest_date}")
        return latest_date
    else:
        pipeline_logger.info(
            "No existing records found in destination. Starting from scratch."
        )
        return None


class API_Runner(BaseModel):
    """
    API_Runner is a DLT pipeline class that defines the configuration and
    data sources for fetching NBA player analytics data from a REST API.
    It uses backoff to handle request failures and ensures robust data extraction.

    Args:
        pipeline_name (str): The name of the DLT pipeline.
        destination_schema (str): The schema in the destination where the data will be stored.
        full_refresh (bool): A flag to indicate whether to perform a full refresh of the data.
        runtime_config (RuntimeConfig): Configuration parameters for the API, including base URL, API key, and team ID.
        start_date (str | None): The starting date for incremental loading. If None, the pipeline will load all available data.
    """

    pipeline_name: str = "nba_player_analytics"
    destination_schema: str
    full_refresh: bool = False
    runtime_config: RuntimeConfig
    start_date: str | None = None

    def sources(self) -> dict[str, dlt.sources.DltSource]:
        """
        Defines the data sources for the DLT pipeline, including API endpoints and parameters.
        Utilizes backoff to handle potential request failures gracefully.
        """

        WRITE_DISPOSITION = "replace" if self.full_refresh else "merge"
        BASE_URL = self.runtime_config.base_url
        HEADERS = {"Authorization": self.runtime_config.api_key}

        pipeline_logger.info("Fetching all games for cache")
        all_games = _fetch_all_games(
            BASE_URL, HEADERS, self.runtime_config.team_id, self.start_date
        )
        game_ids = [g["id"] for g in all_games]
        pipeline_logger.info(f"Found {len(all_games)} games to process")

        @dlt.resource(write_disposition=WRITE_DISPOSITION, primary_key="id")
        def players():
            pipeline_logger.info("Fetching player data")
            cursor = None
            while True:
                params = {"team_ids[]": self.runtime_config.team_id, "per_page": 100}
                if cursor:
                    params["cursor"] = cursor
                body = _fetch_page(f"{BASE_URL}/v1/players", HEADERS, params)
                yield body["data"]
                cursor = body.get("meta", {}).get("next_cursor")
                if not cursor:
                    break

        @dlt.resource(write_disposition=WRITE_DISPOSITION, primary_key="id")
        def games():
            pipeline_logger.info("Yielding game data from cache")
            yield all_games

        @dlt.resource(
            write_disposition=WRITE_DISPOSITION,
            primary_key="id",
            name="game_player_stats",
        )
        def game_player_stats():
            for batch in _chunks(game_ids, 25):
                pipeline_logger.info(
                    f"Fetching player stats for {len(batch)} games (IDs {batch[0]}–{batch[-1]})"
                )
                cursor = None
                while True:
                    params: list = [("game_ids[]", gid) for gid in batch] + [
                        ("per_page", 100)
                    ]
                    if cursor:
                        params.append(("cursor", cursor))
                    body = _fetch_page(f"{BASE_URL}/v1/stats", HEADERS, params)
                    yield body["data"]
                    cursor = body.get("meta", {}).get("next_cursor")
                    if not cursor:
                        break

        @dlt.resource(
            write_disposition=WRITE_DISPOSITION,
            primary_key="id",
            name="game_advanced_stats",
        )
        def game_advanced_stats():
            for batch in _chunks(game_ids, 25):
                pipeline_logger.info(
                    f"Fetching advanced stats for {len(batch)} games (IDs {batch[0]}–{batch[-1]})"
                )
                cursor = None
                while True:
                    params: list = [("game_ids[]", gid) for gid in batch] + [
                        ("per_page", 100),
                        ("period", "0"),
                    ]
                    if cursor:
                        params.append(("cursor", cursor))
                    body = _fetch_page(
                        url=f"{BASE_URL}/nba/v2/stats/advanced",
                        headers=HEADERS,
                        params=params,
                    )
                    yield body["data"]
                    cursor = body.get("meta", {}).get("next_cursor")
                    if not cursor:
                        break

        return {
            "players": players(),
            "games": games(),
            "game_player_stats": game_player_stats(),
            "game_advanced_stats": game_advanced_stats(),
        }

    def load(self, target_endpoint: str | None = None) -> None:
        """
        Initializes the DLT pipeline and runs it with the defined sources.
        """

        pipeline = dlt.pipeline(
            pipeline_name=self.pipeline_name,
            destination="bigquery",
            dataset_name=self.destination_schema,
        )

        available_sources = self.sources()
        if target_endpoint:
            if target_endpoint not in available_sources:
                raise ValueError(
                    f"Invalid target endpoint '{target_endpoint}'. Available endpoints: {list(available_sources.keys())}"
                )
            pipeline_logger.info(
                f"Running pipeline for target endpoint: {target_endpoint}"
            )
            load_info = pipeline.run(available_sources[target_endpoint])
        else:
            pipeline_logger.info("Running pipeline for all endpoints")
            load_info = pipeline.run(self.sources())

        pipeline_logger.info(load_info)
