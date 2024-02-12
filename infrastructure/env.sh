#!/bin/bash
env_file="../development.env"

if [ -f $env_file ]; then
    echo "Writing development.env to ephemeral environment..."
    export $(cat ../development.env)
else
    echo "Can't locate file at ${env_file}"
fi