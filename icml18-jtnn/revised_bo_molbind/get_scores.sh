#!/bin/bash

# do some fancy magic
#
# $1 is current iteration, call this X
# $2 is current seed, call this Y

mkdir etc

# insure mgltools pathing is right
cd mgltools_x86_64Linux2_1.5.6
./install.sh
cd ..

# gnerate pdbqts from pdbs
cd lig_pdbqts$2
for f in $(ls ../lig_pdbs${2}/iter${1}*)
do
    echo $f
    ../mgltools_x86_64Linux2_1.5.6/bin/pythonsh ../mgltools_x86_64Linux2_1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_ligand4.py -l $f -d ../etc/ligand_dict.py
done


# generate vina dockings from pdbqts
cd ..
cd vina_dockings$2
for f in $(ls ../lig_pdbqts${2}/iter${1}*)
do
    echo $f
    export name=$(basename $f .pdbqt)
    echo $name
    mkdir "${name}_6LU7"
    cd "${name}_6LU7"
    echo $f
    cp ../$f .
    vina --config ../../config_6LU7 --ligand "${name}.pdbqt" --receptor ../../6LU7_noligand.pdbqt --log "${name}.log"
    cd ..
    mkdir "${name}_1h4w"
    cd "${name}_1h4w"
    echo $f
    cp ../$f .
    vina --config ../../config_1h4w --ligand "${name}.pdbqt" --receptor ../../1h4w.pdbqt --log "${name}.log"
    cd ..
done


# generate nnscores from vina dockings
cd ..
cd nnscores$2
for f in $(ls ../vina_dockings${2}/*6LU7/iter${1}*_out.pdbqt)
do
    echo $f
    export name=$(basename $f .pdbqt)
    python3 ../nnscore2-2.02/NNScore2.py -ligand $f -receptor ../6LU7_noligand.pdbqt -vina_executable /usr/bin/vina > "${name}_6LU7.log"
done

for f in $(ls ../vina_dockings${2}/*1h4w/iter${1}*_out.pdbqt)
do
    echo $f
    export name=$(basename $f .pdbqt)
    python3 ../nnscore2-2.02/NNScore2.py -ligand $f -receptor ../1h4w.pdbqt -vina_executable /usr/bin/vina > "${name}_1h4w.log"
done





