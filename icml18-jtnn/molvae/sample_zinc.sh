#!/bin/bash

export PYTHONPATH=$HOME/Workspace/icml18-jtnn/

python sample.py --nsample 30000 --vocab ../data/zinc/vocab.txt --hidden 450 --depth 3 --latent 56 --model MPNVAE-h450-L56-d3-beta0.005/model.iter-4 > mol_samples_zinc.txt
