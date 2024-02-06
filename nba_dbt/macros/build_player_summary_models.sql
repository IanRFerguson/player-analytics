{% macro build_player_summary_models(player_id) %}
WITH 
    base AS (
        SELECT
            
            date_trunc(game_.game_date, month) AS month_,
            aggregate_.minutes,
            aggregate_.points,
            aggregate_.field_goal_percentage,
            aggregate_.three_point_percentage,
            aggregate_.effective_field_goal_percentage,
            aggregate_.assists,
            aggregate_.steals,
            aggregate_.blocks,
            aggregate_.turnovers,
            aggregate_.plus_minus,
            aggregate_.offensive_rebounds,
            aggregate_.defensive_rebounds,
            aggregate_.total_rebounds,
            aggregate_.net_rating,
            aggregate_.usage_percentage,
            aggregate_.pace_per_40,

        FROM {{ ref("stg_player__aggregate") }} AS aggregate_
        LEFT JOIN {{ ref("stg_team__game_log") }} AS game_
            USING(game_id)
        WHERE player_id = {{ player_id }}
        ORDER BY month_ ASC
        )

    SELECT

        base.month_,
        ROUND(AVG(base.minutes), 2) AS average_minutes,
        ROUND(AVG(base.points), 2) AS average_points,
        ROUND(AVG(base.field_goal_percentage), 2) AS average_field_goal_percentage,
        ROUND(AVG(base.three_point_percentage), 2) AS average_three_point_percentage,
        ROUND(AVG(base.effective_field_goal_percentage), 2) AS average_effective_field_goal_percentage,
        ROUND(AVG(base.assists), 2) AS average_assists,
        ROUND(AVG(base.steals), 2) AS average_steals,
        ROUND(AVG(base.blocks), 2) AS average_blocks,
        ROUND(AVG(base.turnovers), 2) AS average_turnovers,
        ROUND(AVG(base.plus_minus), 2) AS average_plus_minus,
        ROUND(AVG(base.offensive_rebounds), 2) AS average_offensive_rebounds,
        ROUND(AVG(base.defensive_rebounds), 2) AS average_defensive_rebounds,
        ROUND(AVG(base.total_rebounds), 2) AS average_total_rebounds,
        ROUND(AVG(base.net_rating), 2) AS average_net_rating,
        ROUND(AVG(base.usage_percentage), 2) AS average_usage_percentage,
        ROUND(AVG(base.pace_per_40), 2) AS average_pace_per_40,

    FROM base
    GROUP BY 1
    ORDER BY 1 ASC
{% endmacro %}