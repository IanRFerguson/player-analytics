WITH
    base AS (
        SELECT

            *,
            PARSE_DATE('%b %d, %Y', game_date) AS game_date__parsed,
            LAG(PARSE_DATE('%b %d, %Y', game_date)) OVER (ORDER BY PARSE_DATE('%b %d, %Y', game_date) ASC) AS last_game_date,
            CASE
                WHEN LOWER(matchup) LIKE '%vs%' THEN 'HOME'
                WHEN LOWER(matchup) LIKE '%@%' THEN 'AWAY'
                ELSE NULL
            END AS game_location,
            {{ matchup_opponent('matchup' ) }} AS opponent,
            {{ dbt_utils.generate_surrogate_key(["team_id", "game_id", "matchup"]) }} AS game_log_unique_id

        FROM {{ ref("base_team__game_log") }}
    ),

    game_metadata AS (
        SELECT

            *,
            DATE_DIFF(game_date__parsed, last_game_date, DAY) AS days_between_games,
            CASE
                WHEN DATE_DIFF(game_date__parsed, last_game_date, DAY) IS NULL
                    THEN 0
                WHEN DATE_DIFF(game_date__parsed, last_game_date, DAY) = 1
                    THEN 1
                ELSE 0
            END AS is_back_to_back
            
        FROM base
    ),

    staging AS (

        SELECT

            team_id,
            game_id,
            game_date__parsed AS game_date,
            days_between_games,
            is_back_to_back,
            matchup,
            game_location,
            opponent,
            outcome__win_loss,
            CASE
                WHEN outcome__win_loss = 'W' THEN 1
                WHEN outcome__win_loss = 'L' THEN 0
                ELSE NULL
            END AS outcome__bin,
            outcome__net_wins,
            outcome__net_losses,
            outcome__win_percentage,
            field_goals__made,
            field_goals__attempts,
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
            game_log_unique_id

        FROM game_metadata
    )

SELECT * FROM staging