#!/bin/bash

# This script is run in the local computer to run experiments on the client side and the server side.
# This code builds and compose ups the containers and runs experiment.sh scripts
# Sometimes the experiment numbers in the prints don't match but it's not a problem.

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
