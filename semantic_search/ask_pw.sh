#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Error: No query provided."
    exit 1
fi

query=$1

python3 run_gpt.py "$query"