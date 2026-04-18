import os

from pydantic import BaseModel

#####


class RuntimeConfig(BaseModel):
    base_url: str = "https://api.balldontlie.io"
    api_key: str = os.environ["BALL_DONT_LIE_API_KEY"]

    # NOTE: This is the team ID for the New York Knicks in the balldontlie API.
    # You can change this to analyze a different team.
    team_id: int = 20
