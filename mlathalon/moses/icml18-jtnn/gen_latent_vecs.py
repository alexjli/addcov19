import torch
import torch.nn as nn

import math, random, sys
import argparse
from fast_jtnn import *
import rdkit
import numpy as np

lg = rdkit.RDLogger.logger() 
lg.setLevel(rdkit.RDLogger.CRITICAL)

parser = argparse.ArgumentParser()
parser.add_argument('--vocab', required=True)
parser.add_argument('--model', required=True)
parser.add_argument('--smiles', required=True)

parser.add_argument('--hidden_size', type=int, default=450)
parser.add_argument('--latent_size', type=int, default=56)
parser.add_argument('--depthT', type=int, default=20)
parser.add_argument('--depthG', type=int, default=3)

args = parser.parse_args()

vocab = [x.strip("\r\n ") for x in open(args.vocab)] 
vocab = Vocab(vocab)

model = JTNNVAE(vocab, args.hidden_size, args.latent_size, args.depthT, args.depthG)
model.load_state_dict(torch.load(args.model))
model = model.cuda()

torch.manual_seed(0)

with open(args.smiles) as fp:
    smiles_list = [line.strip() for line in fp]

block_size = 500

for i in xrange(0, 30000, block_size):
    print i
    smiles_sublist = smiles_list[i:i+block_size]
    vecs = model.encode_from_smiles(smiles_sublist)
    vecs = vecs.cpu().detach().numpy()

    np.save('latent_vecs/latent_vecs_%d.npy' % int(i/block_size), vecs)
