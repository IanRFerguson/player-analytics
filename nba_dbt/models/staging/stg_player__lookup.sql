WITH
    players_all_games AS (
        SELECT

            game_id,
            player__id,
            player__name

        FROM {{ ref("base_player__traditional") }}
    ),

    game_log AS (
        SELECT

            game_id,
            game_date,
            MAX(game_date) as most_recent_game

        FROM {{ ref("stg_team__game_log") }}
        GROUP BY 1,2
    ),

    latest_game AS (
        SELECT

            team_id,
            MAX(game_date) AS latest_game

        FROM {{ ref("stg_team__game_log") }}
        GROUP BY 1
    ),

    core_meta AS (
        SELECT

            players_all_games.player__id AS id,
            players_all_games.player__name AS name,
            MIN(game_log.game_date) AS first_game_played,
            MAX(game_log.game_date) AS latest_game_played
            -- TODO - Work in progress
            -- CASE
            --     WHEN MAX(game_log.game_date) IN (SELECT latest_game FROM latest_game) THEN 1
            --     ELSE 0
            -- END AS is_active_player

        FROM players_all_games
        LEFT JOIN game_log
            USING(game_id)
        GROUP BY 1,2
    )

SELECT * FROM core_meta