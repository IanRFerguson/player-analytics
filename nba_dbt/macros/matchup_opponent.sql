{%- macro matchup_opponent(field) -%} 
    CASE
        WHEN LOWER({{field}}) LIKE '%vs%' THEN SPLIT({{field}}, 'vs.')[1]
        WHEN LOWER({{field}}) LIKE '%@%' THEN SPLIT({{field}}, '@')[1]
    END
{%- endmacro -%}