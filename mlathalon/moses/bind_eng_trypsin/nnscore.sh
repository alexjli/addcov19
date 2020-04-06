#!/bin/bash

export base=$PWD

mkdir nnscores
cd nnscores

for (( i=$((2500*$1)); i<$((2500*$1+2500)); i++ ))
do
    echo $i
    export f="../vina_dockings/lig${i}_1h4w/lig${i}_out.pdbqt"
    echo $f
    export name=$(basename $f .pdbqt)
    python3 ../nnscore2-2.02/NNScore2.py -ligand $f -receptor ../1h4w.pdbqt -vina_executable /usr/bin/vina > $name.log
done
