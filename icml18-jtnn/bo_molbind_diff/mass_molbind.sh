#!/bin/bash

for SEED in {1..10}
do
    echo $SEED
    mkdir results$SEED
    python run_bo_molbind.py --vocab ../data/moses/vocab.txt --hidden 450 --latent 56 --seed $SEED --save_dir results$SEED --model ../fast_molvae/moses-h450z56/model.iter-700000
done
