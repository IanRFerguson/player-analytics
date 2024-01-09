import json
import pandas as pd
from nba_api.stats.endpoints.teamgamelog import TeamGameLog

#####


def get_game_data(team_id: str = "1610612752"):
    """
    Hits the NBA API and returns dataframe of all games that
    have already been played this season
    """

    # Get all previous games
    games_ = json.loads(TeamGameLog(1610612752).get_json())["resultSets"]

    # Shape into tabular data
    data_ = pd.DataFrame(games_["rowSet"], columns=games_["headers"])

    return data_


def get_boxscore_data(target: str):
    """
    Retrives player data for a given date. If the Knicks
    did not play a game on this date, the function
    returns `None`
    """

    pass


def clean_player_data(player_data: pd.DataFrame):
    """
    Performs basic cleaning to prepare the dataset
    for the warehouse
    """

    pass
