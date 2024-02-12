# NBA Player Analytics

<img src=".local/nba_dbt.png" width=50%>

This analytics pipeline is composed of the following steps:

* **EXTRACT** - Data is procured from the NBA's API (*see `src/api_helpers.py`*)
* **LOAD** - Data is loaded into BigQuery via a custom wrapper (*see `src/utilities/bigquery.py`*)
* **TRANSFORM** - Raw BigQuery data is cleaned and reshaped with `dbt` (*see `nba_dbt/`*)

<img src=".local/DAG.png" width=75%>

## Source Code

You'll need a Google service account stored locally - `./service_accounts/nba-player-analytics-service.json` ... this is used by every service!

### Infrastructure

The core cloud infrastructure is managed via Terraform in the `infrastructure/` directory. Configuration, production and development datasets, a production Cloud Run service, and all the relevant IAM permissions are managed here. To run this locally, ensure you have a `infrastructure/local.json` file defined like:

```
{
    "USER_EMAIL": "<FILL>",
    "SERVICE_ACCOUNT": "<FILL>",
    "DOCKER_IMAGE_NAME": "<FILL>"
}
```

### Deployment

You'll find production and development Dockerfiles in the `deploy/` directory. You can `docker compose up --build -d` from the root of this project to build the dev environment; I've included a shell script to open an interactive terminal to test things out.

The big difference here is that DEV sleeps infinitely, so it just sits idly and waits for a command. PROD runs a series of commands (defined in `deploy/entrypoint.sh`) to authenticate the shell and connect it to Prefect Cloud.

### Extract + Load

This is all wrapped in `src/run.py`. There are optional CLI arguments to run this locally (outside the cloud context), with a debugger, fully refreshing the data, etc... see `src/utilities/cli.py` for a full list. 

This project IS hardcoded to run Knicks data, because frankly that's all I cared to do!

### Transform

All of the data transformations are handled by dbt - see `nba_dbt/README.md` for a quick mapping. Transformations happen in `staging/`, aggregations and splits happen in `clean/` and individual players are modeled in `player_summaries/`

## Fun Next Steps

* Pull this data into a React app to serve as a dashboard. Player dropdown, stat dropdown, all team stats, etc.
* Train some simple ML models to predict team success as a factor of individual stats and conditions
  * Team offensive rating when Jalen plays > 30 minutes?
  * Defense against top-4 seeds when playing back to back games?
