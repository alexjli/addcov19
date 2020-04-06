#!/bin/bash

mkdir vina_dockings
cd vina_dockings

for f in $(ls ../lig_pdbqts/*)
do
    export name=$(basename $f .pdbqt)
    echo $name
    mkdir "${name}_1h4w"
    cd "${name}_1h4w"
    echo $f
    cp ../$f .
    vina --config ../../config --ligand "${name}.pdbqt" --receptor ../../1h4w.pdbqt --log "${name}.log"
    cd ..
done
