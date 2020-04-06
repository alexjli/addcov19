#!/bin/bash

export base=$PWD

mkdir nnscores
cd nnscores

for f in $(ls ../vina_dockings/*/*_out.pdbqt)
do
    export name=$(basename $f .pdbqt)
    python3 ../nnscore2-2.02/NNScore2.py -ligand $f -receptor ../1h4w.pdbqt -vina_executable /usr/bin/vina > $name.log
done
