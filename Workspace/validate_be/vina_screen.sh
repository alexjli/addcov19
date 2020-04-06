#!/bin/bash

mkdir vina_dockings
cd vina_dockings

for f in $(ls ../lig_pdbqts/*)
do
    export name=$(basename $f .pdbqt)
    echo $name
    mkdir "${name}_6LU7"
    cd "${name}_6LU7"
    echo $f
    cp ../$f .
    vina --config ../../config --ligand "${name}.pdbqt" --receptor ../../6LU7_noligand.pdbqt --log "${name}.log"
    cd ..
done
