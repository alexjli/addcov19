#!/bin/bash
env PYTHONPATH=$HOME/icml18-jtnn python2 sample.py --nsample 30000 --vocab ../data/moses/vocab.txt --hidden 450 --model moses-h450z56/model.iter-700000 > mol_samples.txt
