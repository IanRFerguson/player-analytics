WITH
    base AS (
        SELECT

            {{ easy_alias('Team_ID', 'team_id' ) }},
            {{ easy_alias('Game_ID', 'game_id' ) }},
            {{ easy_alias('GAME_DATE', 'game_date' ) }},
            {{ easy_alias('MATCHUP', 'matchup' ) }},
            {{ easy_alias('WL', 'outcome__win_loss' ) }},
            {{ easy_alias('W', 'outcome__net_wins' ) }},
            {{ easy_alias('L', 'outcome__net_losses' ) }},
            {{ easy_alias('W_PCT', 'outcome__win_percentage' ) }},
            {{ easy_alias('MIN', 'minutes' ) }},
            {{ easy_alias('FGM', 'field_goals__made' ) }},
            {{ easy_alias('FGA', 'field_goals__attemps' ) }},
            {{ easy_alias('FG_PCT', 'field_goals__percentage' ) }},
            {{ easy_alias('FG3M', 'three_pointers__made' ) }},
            {{ easy_alias('FG3A', 'three_pointers__attempts' ) }},
            {{ easy_alias('FG3_PCT', 'three_pointers__percentage' ) }},
            {{ easy_alias('FTM', 'free_throws__made' ) }},
            {{ easy_alias('FTA', 'free_throws__attempts' ) }},
            {{ easy_alias('FT_PCT', 'free_throws__percentage' ) }},
            {{ easy_alias('OREB', 'rebounds__offensive' ) }},
            {{ easy_alias('DREB', 'rebounds__defensive' ) }},
            {{ easy_alias('REB', 'rebounds__total' ) }},
            {{ easy_alias('AST', 'assists' ) }},
            {{ easy_alias('STL', 'steals' ) }},
            {{ easy_alias('BLK', 'blocks' ) }},
            {{ easy_alias('TOV', 'turnovers' ) }},
            {{ easy_alias('PF', 'personal_fouls' ) }},
            {{ easy_alias('PTS', 'points' ) }}

        FROM {{ source('raw_nyk', 'game_log') }}
    )

SELECT * FROM base