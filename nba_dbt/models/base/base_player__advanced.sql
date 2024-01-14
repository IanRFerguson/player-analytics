WITH
    base AS (
        SELECT

            {{ easy_alias('gameId', 'game_id') }},
            {{ easy_alias('teamId', 'team_id') }},
            {{ easy_alias('teamCity', 'city') }},
            {{ easy_alias('teamName', 'team_name') }},
            {{ easy_alias('teamTricode', 'team_abbreviation') }},
            {{ easy_alias('teamSlug', 'team_slug') }},
            {{ easy_alias('personId', 'player__id') }},
            {{ easy_alias('firstName', 'player__first_name') }},
            {{ easy_alias('familyName', 'player__last_name') }},
            {{ easy_alias('nameI', 'player__abbreviation') }},
            {{ easy_alias('playerSlug', 'player__slug') }},
            {{ easy_alias('position', 'player__start_position') }},
            {{ easy_alias('comment', 'player__comment') }},
            {{ easy_alias('jerseyNum', 'player__jersey_number') }},
            {{ easy_alias('minutes', 'minutes') }},
            {{ easy_alias('estimatedOffensiveRating', 'rating__estimated_offensive') }},
            {{ easy_alias('offensiveRating', 'rating__offensive') }},
            {{ easy_alias('estimatedDefensiveRating', 'rating__estimated_defensive') }},
            {{ easy_alias('defensiveRating', 'rating__defensive') }},
            {{ easy_alias('estimatedNetRating', 'rating__estimated_net') }},
            {{ easy_alias('netRating', 'rating__net') }},
            {{ easy_alias('assistPercentage', 'assist__percentage') }},
            {{ easy_alias('assistToTurnover', 'assist__to_turnover') }},
            {{ easy_alias('assistRatio', 'assist__ratio') }},
            {{ easy_alias('offensiveReboundPercentage', 'rebound__offensive_percentage') }},
            {{ easy_alias('defensiveReboundPercentage', 'rebound__defensive_percentage') }},
            {{ easy_alias('reboundPercentage', 'rebound__percentage') }},
            {{ easy_alias('turnoverRatio', 'turnover_ratio') }},
            {{ easy_alias('effectiveFieldGoalPercentage', 'effective_field_goal_percentage') }},
            {{ easy_alias('trueShootingPercentage', 'true_shooting_percentage') }},
            {{ easy_alias('usagePercentage', 'uasge_percentage') }},
            {{ easy_alias('estimatedUsagePercentage', 'usage_percentage__estimated') }},
            {{ easy_alias('estimatedPace', 'pace__estimated') }},
            {{ easy_alias('pace', 'pace') }},
            {{ easy_alias('pacePer40', 'pace__per_40') }},
            possessions,
            {{ easy_alias('PIE', 'player_impact_estimate') }}

        FROM {{ source('raw_nyk', 'box_score__advanced') }}
    )

SELECT * FROM base