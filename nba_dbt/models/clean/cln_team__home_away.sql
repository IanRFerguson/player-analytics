WITH
    base AS (
        SELECT

            game_location,
            ROUND(SUM(outcome__bin) / COUNT(game_id), 2) AS win_percentage,
            ROUND(AVG(points), 2) AS avg_points,
            ROUND(AVG(field_goals__attempts), 2) AS avg_field_goal_attempts,
            ROUND(AVG(field_goals__percentage), 2) AS avg_field_goal_percentage,
            ROUND(AVG(three_pointers__attempts), 2) AS avg_three_point_attempts,
            ROUND(AVG(three_pointers__percentage), 2) AS avg_three_point_percentage,
            ROUND(AVG(rebounds__offensive), 2) AS avg_offensive_rebounds,
            ROUND(AVG(rebounds__defensive), 2) AS avg_defensive_rebounds,
            ROUND(AVG(assists), 2) AS avg_assists,
            ROUND(AVG(steals), 2) AS avg_steals,
            ROUND(AVG(blocks), 2) AS avg_blocks,
            ROUND(AVG(turnovers), 2) AS avg_turnovers,
            ROUND(AVG(personal_fouls), 2) AS avg_personal_fouls,

        FROM {{ ref("stg_team__game_log") }}
        GROUP BY
            game_location
    )

SELECT * FROM base