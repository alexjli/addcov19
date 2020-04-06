#!/bin/bash

for i in {0..29999}
do
    export f="lig_pdbqts/lig${i}.pdbqt"
    if ! [ -f $f ]
    then
        echo $i
    fi
done
