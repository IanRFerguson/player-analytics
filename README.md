# NBA Player Analytics

This analytics pipeline is composed of the following steps:
* **EXTRACT**
  * NBA Player Data is scraped and cleaned via Python
  * This is orchestrated in Prefect to run on a cadence
  * We want the following raw models
    * Player stats per night
    * Player stats on the season (averages)
* **LOAD**
  * The resulting tabular data is loaded into `BigQuery` as a raw table
* **TRANSFORM**
  * Data is aggregated and transofmred via `dbt`
  * We want to represent the following as cleaned `dbt` models
    * Team shooting percentages
    * Team defensive rating vs. opponents