#!/bin/bash

for SEED in 8 9 10
do
    mkdir results$SEED
    python run_bo_molbind.py --vocab ../data/zinc/vocab.txt --hidden 450 --latent 56 --seed $SEED --save_dir results$SEED --model ../molvae/MPNVAE-h450-L56-d3-beta0.005/model.iter-4
done
