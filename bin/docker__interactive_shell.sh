#!/bin/bash
# Run this from the root directory only
wd=`basename $PWD`
if [ ! $wd == "player-analytics" ]; then
    echo "NOTE: Please run this from the root directory of the project"
    exit 1
fi

docker compose exec -it player_analytics bash