{%- macro easy_alias(source_name, dest_name=none) -%}
    {%- if dest_name -%}
    {{ source_name }} AS {{ dest_name }}
    {%- else -%}
    {{ source_name }}
    {%- endif -%}
{%- endmacro -%}