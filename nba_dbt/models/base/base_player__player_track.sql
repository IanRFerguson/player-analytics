WITH
    base AS (
        SELECT

            {{ easy_alias('GAME_ID', 'game_id') }},
            {{ easy_alias('TEAM_ID', 'team_id') }},
            {{ easy_alias('TEAM_ABBREVIATION', 'team_abbreviation') }},
            {{ easy_alias('TEAM_CITY', 'team_city') }},
            {{ easy_alias('PLAYER_ID', 'player__id') }},
            {{ easy_alias('PLAYER_NAME', 'player__name') }},
            {{ easy_alias('START_POSITION', 'player__start_position') }},
            {{ easy_alias('COMMENT', 'player__comment') }},
            {{ easy_alias('MIN', 'minutes') }},
            {{ easy_alias('SPD', 'speed') }},
            {{ easy_alias('DIST', 'distance') }},
            {{ easy_alias('ORBC', 'orbc') }},
            {{ easy_alias('DRBC', 'drbc') }},
            {{ easy_alias('RBC', 'rbc') }},
            {{ easy_alias('TCHS', 'touches') }},
            {{ easy_alias('SAST', 'sast') }},
            {{ easy_alias('FTAST', 'ftast') }},
            {{ easy_alias('PASS', 'passes') }},
            {{ easy_alias('AST', 'assists') }},
            {{ easy_alias('CFGM', 'contested_field_goals__made') }},
            {{ easy_alias('CFGA', 'contested_field_goals__attempted') }},
            {{ easy_alias('CFG_PCT', 'contested_field_goals__percentage') }},
            {{ easy_alias('UFGM', 'uncontested_field_goals__made') }},
            {{ easy_alias('UFGA', 'uncontested_field_goals__attempted') }},
            {{ easy_alias('UFG_PCT', 'unconstested_field_goals__percentage') }},
            {{ easy_alias('FG_PCT', 'field_goals__percentage') }},
            {{ easy_alias('DFGM', 'defended_field_goals__made') }},
            {{ easy_alias('DFGA', 'defended_field_goals__attempted') }},
            {{ easy_alias('DFG_PCT', 'defended_field_goals__percentage') }}

        FROM {{ source('raw_nyk', 'box_score__player_track') }}
    )

SELECT * FROM base