#!/bin/bash

export PYTHONPATH=$PWD
conda init bash
conda activate jtnn_env
cd revised_bo_molbind_diff
mkdir results$1
python run_bo_molbind_revised.py --vocab ../data/moses/vocab.txt --hidden 450 --latent 56 --seed $1 --save_dir results$1 --model ../fast_molvae/moses-h450z56/model.iter-700000
