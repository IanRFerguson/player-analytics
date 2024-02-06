#!/bin/bash

DOCKER_IMAGE_NAME=$1
STAGE=$2

if [ $STAGE == "--prod" ]; then
    echo "Using production image..."
    DOCKERFILE="deploy/Dockerfile.prod"
else
    DOCKERFILE="deploy/Dockerfile.dev"
fi


# Always run this from root
if [ ! -f $DOCKERFILE ]; then
    echo "Dockerfile location is misconfigured..."
    exit 1
fi

# Build container
docker build .  \
    -t $DOCKER_IMAGE_NAME \
    -f $DOCKERFILE \
    --platform=linux/amd64

# Push to Docker hub
docker push $DOCKER_IMAGE_NAME:latest