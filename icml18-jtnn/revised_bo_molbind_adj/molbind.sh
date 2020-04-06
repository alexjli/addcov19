#!/bin/bash


conda init bash
conda activate jtnn_env
export SEED=1
mkdir results$SEED
python run_bo_molbind_revised.py --vocab ../data/moses/vocab.txt --hidden 450 --latent 56 --seed $SEED --save_dir results$SEED --model ../fast_molvae/moses-h450z56/model.iter-700000
