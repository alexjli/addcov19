#!/bin/bash

# use the prepare_ligand4.py script to create pdbqt files
cd lig_pdbqts
for f in $(ls -r ../lig_pdbs/*) 
do
  echo $f
  $HOME/MGLTools-1.5.6/bin/pythonsh $HOME/MGLTools-1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_ligand4.py -l $f -d ../etc/ligand_dict.py
done
