#!/bin/bash

export PYTHONPATH=$HOME/Workspace/icml18-jtnn

python sample.py --nsample 30000 --vocab ../data/moses/vocab.txt --hidden 450 --depth 3 --latent 56 --stereo 0 --model moses-h450L56d3beta0.5/model.iter-2 > mol_samples.txt
