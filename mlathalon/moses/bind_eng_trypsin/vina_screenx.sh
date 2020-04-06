#!/bin/bash

export base=$PWD

mkdir vina_dockings
cd vina_dockings

for (( i=21641; i>=20534; i-- ))
do
    export f="../lig_pdbqts/lig$i.pdbqt"
    export name=$(basename $f .pdbqt)
    echo $name
    mkdir "${name}_1h4w"
    cd "${name}_1h4w"
    echo $f
    ls ../$f
    cp ../$f .
    pwd
    ls ../ | grep config
    vina --config ../config --ligand "${name}.pdbqt" --log "${name}.log"
    cd ..
done
