#!/bin/bash

# do some fancy magic
#
# $1 is current iteration, call this X


# gnerate pdbqts from pdbs
cd lig_pdbqts
for f in $(ls ../lig_pdbs/*)
do
    echo $f
    # generate pdbqts
done


# generate vina dockings from pdbqts
cd ..
cd vina_dockings
for f in $(ls ../lig_pdbqts/*)
do
    echo $f
    # generate vina dockings
done


# generate nnscores from vina sockings
cd ..
cd nnscores
for f in $(ls ../vina_dockings/*)
do
    echo $f
    # generate nnscores
done




