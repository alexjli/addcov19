#!/bin/bash

python gen_latent_fast.py --data ../fast_molvae/mol_samples.txt --vocab ../data/moses/vocab.txt \
--hidden 450 --depth 3 --latent 56 \
--model ../fast_molvae/moses-h450z56/model.iter-700000 
