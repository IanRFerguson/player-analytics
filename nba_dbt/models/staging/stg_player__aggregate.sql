WITH
    traditional AS (
        SELECT

            game_id,
            player__id,
            minutes__cleaned,
            points,
            field_goals__percentage,
            three_point__percentage,
            free_throws__percentage,
            field_goals__attempts,
            three_point__attempts,
            free_throws__attempted,
            rebounds__offensive,
            rebounds__defensive,
            rebounds__total,
            assists,
            steals,
            blocks,
            turnovers,
            personal_fouls,
            plus_minus

        FROM {{ ref("stg_player__traditional") }}
    ),

    scoring AS (
        SELECT

            game_id,
            player__id,
            player__name,

            -- We'd prefer these to be NULL rather than empty strings
            CASE
                WHEN LENGTH(player__start_position) > 0
                    THEN player__start_position
                ELSE NULL
            END AS player__start_position,
            
            -- Infer whether or not a player started on a given night
            CASE
                WHEN LENGTH(player__start_position) > 0
                    THEN 1
                ELSE 0
            END AS player__started,
            
            distribution__from_two,
            distribution__from_three,
            points__from_two,
            points__from_three,
            points__from_free_throws,
            points__off_turnovers,
            points__paint

        FROM {{ ref("stg_player__scoring") }}
    ),

    player_track AS (
        SELECT

            game_id,
            player__id,
            speed,
            distance,
            touches,
            passes,
            contested_field_goals__percentage,
            unconstested_field_goals__percentage,
            defended_field_goals__percentage

        FROM {{ ref("stg_player__player_track") }}
    ),

    advanced AS (
        SELECT

            game_id,
            player__id,
            rating__net,
            rating__offensive,
            rating__defensive,
            assist__ratio,
            assist__to_turnover,
            assist__percentage,
            turnover_ratio,
            effective_field_goal_percentage,
            true_shooting_percentage,
            usage_percentage,
            pace,
            pace__per_40

        FROM {{ ref("stg_player__advanced") }}
    ),

    base AS (
        SELECT

            traditional.game_id,
            traditional.player__id AS player_id,
            scoring.player__name AS player_name,
            traditional.minutes__cleaned AS minutes,
            scoring.player__started AS player_started,
            scoring.player__start_position AS start_position,

            -- On-court raw
            traditional.points,
            traditional.assists,
            traditional.steals,
            traditional.blocks,
            traditional.turnovers,
            player_track.passes,
            player_track.speed,
            player_track.distance,
            advanced.pace,
            player_track.touches,
            traditional.personal_fouls,
            traditional.plus_minus,
            traditional.rebounds__offensive AS offensive_rebounds,
            traditional.rebounds__defensive AS defensive_rebounds,
            traditional.rebounds__total AS total_rebounds,

            -- Shooting raw
            traditional.field_goals__attempts AS field_goal_attempts,
            traditional.three_point__attempts AS three_point_attempts,
            traditional.free_throws__attempted AS free_throw_attempts,

            -- On-court percentages
            advanced.rating__net AS net_rating,
            advanced.rating__offensive AS offensive_rating,
            advanced.rating__defensive AS defensive_rating,
            advanced.assist__ratio AS assist_ratio,
            advanced.assist__to_turnover AS assist_to_turnover_ratio,
            advanced.assist__percentage AS assist_percentage,
            advanced.turnover_ratio,
            advanced.usage_percentage,
            advanced.pace__per_40 AS pace_per_40,
            
            -- Shooting percentages
            traditional.field_goals__percentage AS field_goal_percentage,
            traditional.three_point__percentage AS three_point_percentage,
            traditional.free_throws__percentage AS free_throw_percentage,
            player_track.contested_field_goals__percentage AS contested_field_goal_percentage,
            player_track.unconstested_field_goals__percentage AS uncontested_field_goal_percentage,
            player_track.defended_field_goals__percentage AS defended_field_goal_percentage, 
            advanced.effective_field_goal_percentage,
            advanced.true_shooting_percentage,
            {{ dbt_utils.generate_surrogate_key(["game_id", "player__id"]) }} AS player_aggregate_id


        FROM traditional
        INNER JOIN scoring USING(player__id, game_id)
        INNER JOIN player_track USING(player__id, game_id)
        INNER JOIN advanced USING(player__id, game_id)
    )

SELECT * FROM base