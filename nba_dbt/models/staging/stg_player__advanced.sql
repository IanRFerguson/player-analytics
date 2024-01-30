WITH
    meta AS (

        SELECT

            *,
            CASE
                WHEN player__comment LIKE '%DNP%' or player__comment LIKE '%DND%' THEN '0:0'
                ELSE minutes
            END AS game_minutes,
            'ADVANCED' AS _model

        FROM {{ ref("base_player__advanced") }}
    ),

    base AS (
        SELECT

            game_id,
            team_id,
            player__id,
            player__first_name,
            player__last_name,
            player__start_position,
            minutes,
            game_minutes,
            {{ convert_player_minutes_to_seconds("game_minutes") }} AS minutes__cleaned,
            rating__net,
            rating__offensive,
            rating__defensive,
            rating__estimated_net,
            rating__estimated_offensive,
            rating__estimated_defensive,
            assist__ratio,
            assist__to_turnover,
            assist__percentage,
            rebound__percentage,
            rebound__offensive_percentage,
            rebound__defensive_percentage,
            turnover_ratio,
            effective_field_goal_percentage,
            true_shooting_percentage,
            usage_percentage,
            pace,
            pace__estimated,
            pace__per_40,
            {{ dbt_utils.generate_surrogate_key(["game_id", "player__id", "_model"]) }} AS advanced_unique_id

        FROM meta
    )

SELECT * FROM base