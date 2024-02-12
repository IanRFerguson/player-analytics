#!/bin/bash
# Allows for optional --build flag to be passed in via command line
extra_command=$1

# Run this from the root directory only
wd=`basename $PWD`
if [ ! $wd == "player-analytics" ]; then
    echo "NOTE: Please run this from the root directory of the project"
    exit 1
fi

echo "Stopping container..."
docker compose down

echo "Restarting container..."
docker compose up -d $1

# Alternatively print rebuild / restart
if [[ $extra_command == "--build" ]]; then
    echo "Docker container successfully rebuilt"
else
    echo "Docker container successfully restarted"
fi