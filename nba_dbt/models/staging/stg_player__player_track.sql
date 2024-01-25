WITH
    meta AS (
        SELECT

            *,
            'PLAYER_TRACK' AS _model
        
        FROM {{ ref("base_player__player_track") }}
    ),

    base AS (
        SELECT

            game_id,
            team_id,
            player__id,
            player__name,
            player__start_position,
            minutes,
            {{ convert_player_minutes_to_seconds("minutes") }} AS minutes__cleaned,
            speed,
            distance,
            touches,
            passes,
            contested_field_goals__made
            contested_field_goals__attempted,
            contested_field_goals__percentage,
            uncontested_field_goals__made,
            uncontested_field_goals__attempted,
            unconstested_field_goals__percentage,
            field_goals__percentage,
            defended_field_goals__made,
            defended_field_goals__attempted,
            defended_field_goals__percentage,
            {{ dbt_utils.generate_surrogate_key(["game_id", "player__id", "_model"]) }} AS player_track_unique_id

        FROM meta
    )

SELECT * FROM base