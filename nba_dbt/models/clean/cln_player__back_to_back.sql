WITH
    games AS (
        SELECT

            game_id,
            is_back_to_back

        FROM {{ ref("stg_team__game_log") }}
    ),

    players AS (
        SELECT

        FROM {{ ref("stg_player__aggregate") }}
    ),

    base AS (
        SELECT

            is_back_to_back,
            player_id,
            player_name,
            AVERAGE(points),
            AVERAGE(minutes),
            SUM(player_started) / COUNT(game_id) AS games_started_percentage

        FROM players
        JOIN games USING(game_id)
        GROUP BY
            is_back_to_back,
            player_id
    )

SELECT * FROM base