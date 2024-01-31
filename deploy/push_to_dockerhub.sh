#!/bin/bash

if [ ! -f "deploy/Dockerfile.dev" ]; then
    echo "Dockerfile location is misconfigured..."
fi

# Static container name
DOCKER_IMAGE_NAME=ianrichardferguson/nba-player-analytics

# Build container
docker build -t $DOCKER_IMAGE_NAME . -f deploy/Dockerfile.dev

# Push to Docker hub
docker push $DOCKER_IMAGE_NAME:latest