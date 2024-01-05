#!/bin/bash

# This script should not but run directly. It is run by experiment_local.sh in local computer.
# This script is used to run the two server scripts in parallel.

RED='\033[0;31m'
NC='\033[0m' # No Color
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'

# Run the first script in the background
./experiment_server_tcp.sh &

# Run the second script in the foreground
./experiment_server_udp.sh

# Wait for all background jobs to complete
wait
echo -e "${YELLOW}\nBoth scripts completed.\n${NC}"
