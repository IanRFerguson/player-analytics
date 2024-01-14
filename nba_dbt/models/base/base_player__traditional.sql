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
            {{ easy_alias('COMMENT', 'player__comment') }},
            {{ easy_alias('MIN', 'minutes') }},
            {{ easy_alias('FGM', 'field_goals__made') }},
            {{ easy_alias('FGA', 'field_goals__attempts') }},
            {{ easy_alias('FG_PCT', 'field_goals__percentage') }},
            {{ easy_alias('FG3M', 'three_point__made') }},
            {{ easy_alias('FG3A', 'three_point__attempts') }},
            {{ easy_alias('FG3_PCT', 'three_point__percentage') }},
            {{ easy_alias('FTM', 'free_throws__made') }},
            {{ easy_alias('FTA', 'free_throws__attempted') }},
            {{ easy_alias('FT_PCT', 'free_throws__percentage') }},
            {{ easy_alias('OREB', 'rebounds__offensive') }},
            {{ easy_alias('DREB', 'rebounds__defensive') }},
            {{ easy_alias('REB', 'rebounds__total') }},
            {{ easy_alias('AST', 'assists') }},
            {{ easy_alias('STL', 'steals') }},
            {{ easy_alias('BLK', 'blocks') }},
            {{ easy_alias('`TO`', 'to_') }}
            {{ easy_alias('PF', 'personal_fouls') }},
            {{ easy_alias('PTS', 'points') }},
            {{ easy_alias('PLUS_MINUS', 'plus_minus') }}

        FROM {{ source('raw_nyk', 'box_score__traditional') }}
    )

SELECT * FROM base