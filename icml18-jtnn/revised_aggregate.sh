#!/bin/bash

# must run with jtnn_env

# making sure directory is correct
#cd ~/Workspace/icml18-jtnn/

# clearing the file if it already exists
if [ -f revised_results.temp ]; then
    echo "removing old file"
    rm revised_results.temp
fi

for f in revised_bo_molbind*/; do
    echo $f
    cd $f
    pwd >> ../revised_results.temp
    python print_result.py >> ../revised_results.temp
    echo "" >> ../revised_results.temp
    cd ..
done

python revised_aggregate_temps.py
rm revised_results.temp
