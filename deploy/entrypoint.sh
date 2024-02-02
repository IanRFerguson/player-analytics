#!/bin/bash

# Authenticate with Prefect Cloud
prefect cloud login \
    --key $PREFECT_API_KEY \
    --workspace $PREFECT_WORKSPACE

# Run ELT workflow
python src/run.py