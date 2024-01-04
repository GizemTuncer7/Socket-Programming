#!/bin/bash

# Define the interface to manipulate
IFACE=eth0

# Experiment configurations
EXPERIMENTS=30
LOSS_RATES=("0%" "5%" "10%" "15%")
DUPLICATION_RATES=("0%" "5%" "10%")
CORRUPTION_RATES=("0%" "5%" "10%")
DELAY_TYPES=("100ms 50ms distribution uniform" "100ms 50ms distribution normal")

# Function to apply network conditions
apply_conditions() {
    sudo tc qdisc add dev $IFACE root netem $1 $2
}

# Function to clear network conditions
clear_conditions() {
    sudo tc qdisc del dev $IFACE root
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
            echo "Running UDP experiment $i with $condition_type $value"
            python3 ../udp_application/udp_client.py
            # Run corresponding server in the background or on another terminal
            # python udp_server.py

            echo "Running TCP experiment $i with $condition_type $value"
            python3 ../tcp_application/tcp_client.py
            # Run corresponding server in the background or on another terminal
            # python tcp_server.py
        done

        # Clear network conditions after the batch is done
        clear_conditions

        # Wait a bit before the next experiment set
        sleep 2
    done
}

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
