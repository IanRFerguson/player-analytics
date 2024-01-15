WITH
    base AS (
        SELECT

            game_id,
            team_id,
            player__id,
            minutes,
            {{ convert_player_minutes_to_seconds("minutes") }} AS minutes__cleaned,
            field_goals__made,
            field_goals__attempts,
            field_goals__percentage,
            three_point__made,
            three_point__attempts,
            three_point__percentage,
            free_throws__made,
            free_throws__attempted,
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
            plus_minus,
            {{ dbt_utils.generate_surrogate_key(["game_id", "player__id"]) }} AS traditional_unique_id

        FROM {{ ref("base_player__traditional") }}
    )

SELECT * FROM base