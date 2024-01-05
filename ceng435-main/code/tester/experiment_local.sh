#!/bin/bash

# Step 1: Build the Docker image
cd ../..

docker build -t ceng435 .

# Check if the build was successful
if [ $? -eq 0 ]; then
    # Step 2: Clear the screen
    clear

    # Step 3: Start up the containers using Docker Compose
    docker compose up
else
    echo "Docker build failed, exiting."
fi
