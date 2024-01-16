WITH
    base AS (
        SELECT

            team_id,
            game_id,
            game_date,
            matchup,
            CASE
                WHEN LOWER(matchup) LIKE '%vs%' THEN 'HOME'
                WHEN LOWER(matchup) LIKE '%@%' THEN 'AWAY'
                ELSE NULL
            END AS game_location,
            {{ matchup_opponent('matchup' )}} AS opponent,
            outcome__win_loss,
            outcome__net_wins,
            outcome__net_losses,
            outcome__win_percentage,
            field_goals__made,
            field_goals__attemps,
            field_goals__percentage,
            three_pointers__made,
            three_pointers__attempts,
            three_pointers__percentage,
            free_throws__made,
            free_throws__attempts,
            free_throws__percentage,
            rebounds__offensive,
            rebounds__defensive,
            rebounds__total,
            assists,
            steals,
            blocks,
            turnovers,
            personal_fouls,
            points,
            {{ dbt_utils.generate_surrogate_key(["team_id", "game_id", "matchup"]) }} AS game_log_unique_id

        FROM {{ ref("base_team__game_log") }}
    )

SELECT * FROM base