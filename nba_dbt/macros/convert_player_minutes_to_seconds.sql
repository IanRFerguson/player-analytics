{%- macro convert_player_minutes_to_seconds(value, delimiter=":") -%}
    CAST(SPLIT({{ value }}, '{{ delimiter }}')[0] AS INTEGER) + (CAST(SPLIT({{ value }}, '{{ delimiter }}')[1] AS INTEGER) / 60)
{%- endmacro -%}