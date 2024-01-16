# NBA Player Analytics

<img src=".local/nba_dbt.png" width=75%>

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

## Usage

Run this pipeline locally via Docker:

```
docker compose up --build -d
```

Once the container builds, you can run an interactive shell and execute the source code as you would at the command line on your own machine:

```
# Start interactive shell via Docker compose
bash dev__interactive_shell.sh

# Run the main function "locally"
python src/run.py --full-refresh --local

# Kick the main function off via Prefect
python src/run.py
```