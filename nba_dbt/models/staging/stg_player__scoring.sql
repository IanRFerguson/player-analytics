WITH
    base AS (
        SELECT

            game_id,
            team_id,
            player__id,
            player__name,
            player__start_position,
            distribution__from_two,
            distribution__from_three,
            points__from_two,
            points__from_three,
            points__from_free_throws,
            points__off_turnovers,
            points__paint,
            {{ dbt_utils.generate_surrogate_key(["game_id", "player__id"]) }} AS scoring_unique_id

        FROM {{ ref("base_player__scoring") }}
    )

SELECT * FROM base