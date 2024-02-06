#!/bin/bash

set -e

# Pull run config from BigQuery
python src/pull_config_into_environment.py

# Login to Prefect cloud via CLI
python src/prefect_helpers.py

# Run flow with Prefect cloud
python src/run.py