#!/bin/bash

export base=$PWD

mkdir nnscores
cd nnscores

for f in $(ls ../vina_dockings/*6LU7/*_out.pdbqt)
do
    export name=$(basename $f .pdbqt)
    python3 ../nnscore2-2.02/NNScore2.py -ligand $f -receptor ../6LU7_noligand.pdbqt -vina_executable /usr/local/bin/vina > $name.log
done
