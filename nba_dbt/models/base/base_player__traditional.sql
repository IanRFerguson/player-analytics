WITH
    base AS (
        SELECT

            {{ easy_alias('GAME_ID', '') }},
            {{ easy_alias('TEAM_ID', '') }},
            {{ easy_alias('TEAM_ABBREVIATION', '') }},
            {{ easy_alias('TEAM_CITY', '') }},
            {{ easy_alias('PLAYER_ID', '') }},
            {{ easy_alias('PLAYER_NAME', '') }},
            {{ easy_alias('NICKNAME', '') }},
            {{ easy_alias('START_POSITION', '') }},
            {{ easy_alias('COMMENT', '') }},
            {{ easy_alias('MIN', '') }},
            {{ easy_alias('FGM', '') }},
            {{ easy_alias('FGA', '') }},
            {{ easy_alias('FG_PCT', '') }},
            {{ easy_alias('FG3M', '') }},
            {{ easy_alias('FG3A', '') }},
            {{ easy_alias('FG3_PCT', '') }},
            {{ easy_alias('FTM', '') }},
            {{ easy_alias('FTA', '') }},
            {{ easy_alias('FT_PCT', '') }},
            {{ easy_alias('OREB', '') }},
            {{ easy_alias('DREB', '') }},
            {{ easy_alias('REB', '') }},
            {{ easy_alias('AST', '') }},
            {{ easy_alias('STL', '') }},
            {{ easy_alias('BLK', '') }},
            {{ easy_alias('`TO`', 'to_') }}
            {{ easy_alias('PF', '') }},
            {{ easy_alias('PTS', '') }},
            {{ easy_alias('PLUS_MINUS', '') }}

        FROM {{ source('raw_nyk', 'box_score__traditional') }}
    )

SELECT * FROM base