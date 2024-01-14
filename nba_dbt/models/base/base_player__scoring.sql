WITH
    base AS (
        SELECT

            {{ easy_alias('GAME_ID', 'game_id') }},
            {{ easy_alias('TEAM_ID', 'team_id') }},
            {{ easy_alias('TEAM_ABBREVIATION', 'team_abbreviation') }},
            {{ easy_alias('TEAM_CITY', 'team_city') }},
            {{ easy_alias('PLAYER_ID', 'player__id') }},
            {{ easy_alias('PLAYER_NAME', 'player__name') }},
            {{ easy_alias('NICKNAME', 'player__nickname') }},
            {{ easy_alias('START_POSITION', 'player__start_position') }},
            {{ easy_alias('COMMENT', 'player__comments') }},
            {{ easy_alias('MIN', 'minutes') }},
            {{ easy_alias('PCT_FGA_2PT', 'field_goals__a') }},
            {{ easy_alias('PCT_FGA_3PT', '') }},
            {{ easy_alias('PCT_PTS_2PT', '') }},
            {{ easy_alias('PCT_PTS_2PT_MR', '') }},
            {{ easy_alias('PCT_PTS_3PT', '') }},
            {{ easy_alias('PCT_PTS_FB', '') }},
            {{ easy_alias('PCT_PTS_FT', '') }},
            {{ easy_alias('PCT_PTS_OFF_TOV', '') }},
            {{ easy_alias('PCT_PTS_PAINT', '') }},
            {{ easy_alias('PCT_AST_2PM', '') }},
            {{ easy_alias('PCT_UAST_2PM', '') }},
            {{ easy_alias('PCT_AST_3PM', '') }},
            {{ easy_alias('PCT_UAST_3PM', '') }},
            {{ easy_alias('PCT_AST_FGM', '') }},
            {{ easy_alias('PCT_UAST_FGM', '') }}

        FROM {{ source('raw_nyk', 'box_score__scoring') }}
    )

SELECT * FROM base