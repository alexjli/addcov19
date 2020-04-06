import torch
import torch.nn as nn
import torch.nn.functional as F
from fast_jtnn.mol_tree import Vocab, MolTree
from fast_jtnn.nnutils import create_var, flatten_tensor, avg_pool
from fast_jtnn.jtnn_enc import JTNNEncoder
from fast_jtnn.jtnn_dec import JTNNDecoder
from fast_jtnn.mpn import MPN
from fast_jtnn.jtmpn import JTMPN
from fast_jtnn.datautils import tensorize
from fast_jtnn import *
from fast_jtnn.chemutils import enum_assemble, set_atommap, copy_edit_mol, attach_mols
import rdkit
import rdkit.Chem as Chem
import copy, math
import numpy as np
import argparse

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

num_smiles = len(smiles_list)
print 'Num SMILES', num_smiles
print 'Gen MolTrees'
#tree_batch = [MolTree(s) for s in smiles_list]
tree_batch = []
for i in xrange(num_smiles):
    tree_batch.append(MolTree(smiles_list[i]))
    if i % 1000 == 999:
        print i + 1


batch_size = 500

for i in xrange(num_smiles/batch_size):
    print 'Batch %d' % i
    tree_subbatch = tree_batch[i*batch_size:(i+1)*batch_size]
    print 'Tensorizing'
    _, jtenc_holder, mpn_holder = tensorize(tree_subbatch, model.vocab, assm=False)
    print 'Encoding'
    means, vars = model.encode_latent(jtenc_holder, mpn_holder)
    means = means.cpu().detach().numpy()
    vars = vars.cpu().detach().numpy()
    np.save('latent_means/latent_means_%d.npy' % i, means)
    np.save('latent_means/latent_vars_%d.npy' % i, vars)
