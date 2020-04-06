#!/bin/bash


echo Starting...
echo Collecting results from revised_bo_molbind
cd revised_bo_molbind
python aggregate.py
mv aggregate_results.json ../revised_bo_molbind_results/vanilla.json
cd ..

echo Collecting results from revised_bo_molbind_adj
cd revised_bo_molbind_adj
python aggregate.py
mv aggregate_results.json ../revised_bo_molbind_results/adj.json
cd ..

echo Collecting results from revised_bo_molbind_diff
cd revised_bo_molbind_diff
python aggregate.py
mv aggregate_results.json ../revised_bo_molbind_results/diff.json
cd ..

echo Collecting results from revised_bo_molbind_diff_adj
cd revised_bo_molbind_diff_adj
python aggregate.py
mv aggregate_results.json ../revised_bo_molbind_results/diff_adj.json

echo Done!
