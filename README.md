# NBA Player Analytics

<img src=".local/nba_dbt.png" width=50%>

This analytics pipeline is composed of the following steps:

* **EXTRACT** - Data is procured from the NBA's API (*see `src/api_helpers.py`*)
* **LOAD** - Data is loaded into BigQuery via a custom wrapper (*see `src/utilities/bigquery.py`*)
* **TRANSFORM** - Raw BigQuery data is cleaned and reshaped with `dbt` (*see `nba_dbt/`*)

<img src=".local/DAG.png" width=75%>