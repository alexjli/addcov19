#!/bin/bash

cd vina_dockings

for i in {5000..0}
do
    export f="../lig_pdbqts/lig$i.pdbqt"
    export name=$(basename $f .pdbqt)
    echo $name
    mkdir "${name}_6LU7"
    cd "${name}_6LU7"
    echo $f
    ls ../$f
    cp ../$f .
    vina --config ../config --ligand "${name}.pdbqt" --receptor ../../6LU7_noligand.pdbqt --log "${name}.log"
    cd ..
done
