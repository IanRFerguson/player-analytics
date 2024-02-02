#!/bin/bash

STAGE=$1

if [ $STAGE == "--prod" ]; then
    echo "Using production image..."
    DOCKERFILE="deploy/Dockerfile.dev"
else
    DOCKERFILE="deploy/Dockerfile.prod"
fi


# Always run this from root
if [ ! -f $DOCKERFILE ]; then
    echo "Dockerfile location is misconfigured..."
    exit 1
fi

# Static container name
DOCKER_IMAGE_NAME=ianrichardferguson/nba-player-analytics

# Build container
docker build .  \
    -t $DOCKER_IMAGE_NAME \
    -f $DOCKERFILE \
    --platform=linux/amd64

# Push to Docker hub
docker push $DOCKER_IMAGE_NAME:latest