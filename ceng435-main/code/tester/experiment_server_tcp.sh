#!/bin/bash

# Define the interface to manipulate
IFACE=eth0

# Experiment configurations
EXPERIMENTS=5
LOSS_RATES=("0%" "5%" "10%" "15%")
DUPLICATION_RATES=("0%" "5%" "10%")
CORRUPTION_RATES=("0%" "5%" "10%")
DELAY_TYPES=("100ms uniform distribution" "100ms normal distribution")

RED='\033[0;31m'
NC='\033[0m' # No Color
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'

# Function to apply network conditions
apply_conditions() {
    tc qdisc add dev $IFACE root netem $1 $2
}

# Function to clear network conditions
clear_conditions() {
    tc qdisc del dev $IFACE root
}

# Function to run experiments for a given condition
run_experiments() {
    local condition_type=$1
    local values=("${@:2}")  # Remaining arguments as array

    for value in "${values[@]}"; do
        # Apply network conditions
        apply_conditions "$condition_type" "$value"

        # Run experiments for both UDP and TCP
        for i in $(seq 1 $EXPERIMENTS); do
            echo -e "${RED}Running TCP experiment $i with $condition_type $value on server${NC}"
            python3 ../tcp_application/tcp_server.py
            # Run corresponding server in the background or on another terminal
            # python tcp_server.py

            echo -e "\n"
        done

        # Clear network conditions after the batch is done
        clear_conditions

        # Wait a bit before the next experiment set
        sleep 2
    done

    echo -e "\n\n"
}

# Ensure any existing network conditions are cleared
clear_conditions

# # Benchmarking phase without any network impairments
# echo "Running benchmark experiments (no network impairments)"
# for i in $(seq 1 $EXPERIMENTS); do
#     echo "Running UDP benchmark experiment $i"
#     python3 ../udp_application/udp_client.py
#     # Run corresponding server in the background or on another terminal
#     # python udp_server.py

#     echo "Running TCP benchmark experiment $i"
#     python3 ../tcp_application/tcp_client.py
#     # Run corresponding server in the background or on another terminal
#     # python tcp_server.py
# done

# Now running experiments with network impairments

# Run experiments for packet loss
echo "Running experiments for packet loss"
run_experiments "loss" "${LOSS_RATES[@]}"

# Run experiments for packet duplication
echo "Running experiments for packet duplication"
run_experiments "duplicate" "${DUPLICATION_RATES[@]}"

# Run experiments for packet corruption
echo "Running experiments for packet corruption"
run_experiments "corrupt" "${CORRUPTION_RATES[@]}"

# Run experiments for packet delay
echo "Running experiments for packet delay"
run_experiments "delay" "${DELAY_TYPES[@]}"
