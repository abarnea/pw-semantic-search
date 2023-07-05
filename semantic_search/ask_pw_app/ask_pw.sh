#!/bin/bash

if [ $# -eq 0 ]
then
    echo "Error: No query provided."
    exit 1
fi

query=$1

cd ../core_code
python3 run_gpt.py "$query"