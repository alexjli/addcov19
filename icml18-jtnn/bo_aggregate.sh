#!/bin/bash

# must run with jtnn_env

# making sure directory is correct
cd ~/Workspace/icml18-jtnn/

# clearing the file if it already exists
if [ -f bo_results.temp ]; then
    echo "removing old file"
    rm bo_results.temp
fi

for f in bo_molbind*/; do
    cd $f
    pwd >> ../bo_results.temp
    python print_result.py >> ../bo_results.temp
    echo "" >> ../bo_results.temp
    cd ..
done

python bo_aggregate_temps.py
rm bo_results.temp
