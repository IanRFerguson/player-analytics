import os
from nba_api.stats.endpoints.boxscoreadvancedv3 import BoxScoreAdvancedV3
from nba_api.stats.endpoints.boxscorescoringv2 import BoxScoreScoringV2
from nba_api.stats.endpoints.boxscoreplayertrackv2 import BoxScorePlayerTrackV2
from nba_api.stats.endpoints.boxscoretraditionalv2 import BoxScoreTraditionalV2

#####

TEAM_CONFIG = {"nyk": {"dataset": "raw__nyk_data", "id": "1610612752"}}
LOG_TABLE = "_etl_log"

STAT_TABLE_CONFIG = {
    "box_score__advanced": {
        "raw_table_name": "box_score__advanced",
        "api_endpoint": BoxScoreAdvancedV3,
        "team_id_field": "teamId",
        "ignore_columns": [],
    },
    "box_score__scoring": {
        "raw_table_name": "box_score__scoring",
        "api_endpoint": BoxScoreScoringV2,
        "team_id_field": "TEAM_ID",
        "ignore_columns": ["MIN"],
    },
    "box_score__player_track": {
        "raw_table_name": "box_score__player_track",
        "api_endpoint": BoxScorePlayerTrackV2,
        "team_id_field": "TEAM_ID",
        "ignore_columns": [],
    },
    "box_score__traditional": {
        "raw_table_name": "box_score__traditional",
        "api_endpoint": BoxScoreTraditionalV2,
        "team_id_field": "TEAM_ID",
        "ignore_columns": [],
    },
}
