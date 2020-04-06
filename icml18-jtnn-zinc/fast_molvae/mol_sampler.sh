#!/bin/bash

for model in $(ls vae_model)
do
    python sample.py --nsample 30000 --vocab ../data/zinc/vocab.txt --hidden 450 --model "vae_model/${model}" > smiles/"${model}.mol_samples.txt"
done
