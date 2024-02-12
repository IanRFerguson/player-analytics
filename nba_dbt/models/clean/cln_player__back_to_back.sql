WITH
    games AS (
        SELECT

            game_id,
            is_back_to_back

        FROM {{ ref("stg_team__game_log") }}
    ),

    players AS (
        SELECT

            game_id,
            player_id,
            player_name,
            player_started,
            points,
            assists,
            steals,
            blocks,
            turnovers,
            passes,
            speed,
            distance,
            touches,
            personal_fouls,
            plus_minus,
            offensive_rebounds,
            defensive_rebounds,
            total_rebounds,
            net_rating,
            offensive_rating,
            defensive_rating,
            assist_ratio,
            assist_to_turnover_ratio,
            assist_percentage,
            turnover_ratio,
            usage_percentage,
            pace_per_40,
            field_goal_percentage,
            three_point_percentage,
            free_throw_percentage,
            effective_field_goal_percentage

        FROM {{ ref("stg_player__aggregate") }}
    ),

    base AS (
        SELECT

            player_id,
            player_name,
            is_back_to_back,
            ROUND(SUM(player_started) / COUNT(players.game_id), 2) AS games_started_percentage,
            ROUND(AVG(points), 2) AS avg_points,
            ROUND(AVG(assists), 2) AS avg_assists,
            ROUND(AVG(steals), 2) AS avg_steals,
            ROUND(AVG(blocks), 2) AS avg_blocks,
            ROUND(AVG(turnovers), 2) AS avg_turnovers,
            ROUND(AVG(passes), 2) AS avg_passes,
            ROUND(AVG(speed), 2) AS avg_speed,
            ROUND(AVG(distance), 2) AS avg_distance,
            ROUND(AVG(touches), 2) AS avg_touches,
            ROUND(AVG(personal_fouls), 2) AS avg_personal_fouls,
            ROUND(AVG(plus_minus), 2) AS avg_plus_minus,
            ROUND(AVG(offensive_rebounds), 2) AS avg_offensive_rebounds,
            ROUND(AVG(defensive_rebounds), 2) AS avg_defensive_rebounds,
            ROUND(AVG(total_rebounds), 2) AS avg_total_rebounds,
            ROUND(AVG(net_rating), 2) AS avg_net_rating,
            ROUND(AVG(offensive_rating), 2) AS avg_offensive_rating,
            ROUND(AVG(defensive_rating), 2) AS avg_defensive_rating,
            ROUND(AVG(assist_ratio), 2) AS avg_assist_ratio,
            ROUND(AVG(assist_to_turnover_ratio), 2) AS avg_assist_to_turnover_ratio,
            ROUND(AVG(assist_percentage), 2) AS avg_assist_percentage,
            ROUND(AVG(turnover_ratio), 2) AS avg_turnover_ratio,
            ROUND(AVG(usage_percentage), 2) AS avg_usage_percentage,
            ROUND(AVG(pace_per_40), 2) AS avg_pace_per_40,
            ROUND(AVG(field_goal_percentage), 2) AS avg_field_goal_percentage,
            ROUND(AVG(three_point_percentage), 2) AS avg_three_point_percentage,
            ROUND(AVG(free_throw_percentage), 2) AS avg_free_throw_percentage,
            ROUND(AVG(effective_field_goal_percentage), 2) AS avg_effective_field_goal_percentage,            
            {{ dbt_utils.generate_surrogate_key(["is_back_to_back", "player_id"]) }} AS player_back_to_back_id

        FROM players
        INNER JOIN games ON players.game_id = games.game_id
        GROUP BY
            is_back_to_back,
            player_id,
            player_name
        ORDER BY
            is_back_to_back,
            player_name
    )

SELECT * FROM base