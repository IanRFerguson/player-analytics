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
            {{ easy_alias('PCT_FGA_2PT', 'distribution__from_two') }},
            {{ easy_alias('PCT_FGA_3PT', 'distribution__from_three') }},
            {{ easy_alias('PCT_PTS_2PT', 'points__from_two') }},
            {{ easy_alias('PCT_PTS_2PT_MR', 'pct_pts_2pt_mr') }},
            {{ easy_alias('PCT_PTS_3PT', 'points__from_three') }},
            {{ easy_alias('PCT_PTS_FB', 'pct_pts_fb') }},
            {{ easy_alias('PCT_PTS_FT', 'points__from_free_throws') }},
            {{ easy_alias('PCT_PTS_OFF_TOV', 'points__off_turnovers') }},
            {{ easy_alias('PCT_PTS_PAINT', 'points__paint') }},
            {{ easy_alias('PCT_AST_2PM', 'pct_ast_2pm') }},
            {{ easy_alias('PCT_UAST_2PM', 'pct_uast_2pm') }},
            {{ easy_alias('PCT_AST_3PM', 'pct_ast_3pm') }},
            {{ easy_alias('PCT_UAST_3PM', 'pct_uast_3pm') }},
            {{ easy_alias('PCT_AST_FGM', 'pct_ast_fgm') }},
            {{ easy_alias('PCT_UAST_FGM', 'pct_uast_fgm') }}

        FROM {{ source('raw_nyk', 'box_score__scoring') }}
    )

SELECT * FROM base