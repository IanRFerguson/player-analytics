{%- macro convert_player_minutes_to_seconds(value, delimiter=":") -%}
    CAST(SPLIT({{ value }}, '{{ delimiter }}')[0] AS FLOAT64) + (CAST(SPLIT({{ value }}, '{{ delimiter }}')[1] AS FLOAT64) / 60)
{%- endmacro -%}