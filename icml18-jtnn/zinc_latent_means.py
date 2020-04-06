import torch
import torch.nn as nn
from torch.autograd import Variable
from optparse import OptionParser

import rdkit
from rdkit.Chem import Descriptors
from rdkit.Chem import MolFromSmiles, MolToSmiles
from rdkit.Chem import rdmolops
import sascorer

import numpy as np  
from jtnn import *

lg = rdkit.RDLogger.logger() 
lg.setLevel(rdkit.RDLogger.CRITICAL)

parser = OptionParser()
parser.add_option("-a", "--data", dest="data_path")
parser.add_option("-v", "--vocab", dest="vocab_path")
parser.add_option("-m", "--model", dest="model_path")
parser.add_option("-w", "--hidden", dest="hidden_size", default=200)
parser.add_option("-l", "--latent", dest="latent_size", default=56)
parser.add_option("-d", "--depth", dest="depth", default=3)
opts,args = parser.parse_args()

with open(opts.data_path) as f:
    smiles = f.readlines()

for i in xrange(len(smiles)):
    smiles[ i ] = smiles[ i ].strip()

vocab = [x.strip("\r\n ") for x in open(opts.vocab_path)] 
vocab = Vocab(vocab)

batch_size = 100
hidden_size = int(opts.hidden_size)
latent_size = int(opts.latent_size)
depth = int(opts.depth)

model = JTNNVAE(vocab, hidden_size, latent_size, depth)
model.load_state_dict(torch.load(opts.model_path))
model = model.cuda()

smiles_rdkit = []
for i in xrange(len(smiles)):
    smiles_rdkit.append(MolToSmiles(MolFromSmiles(smiles[ i ]), isomericSmiles=True))

SA_scores = []
for i in xrange(len(smiles)):
    SA_scores.append(-sascorer.calculateScore(MolFromSmiles(smiles_rdkit[ i ])))

import networkx as nx

cycle_scores = []
for i in range(len(smiles)):
    cycle_list = nx.cycle_basis(nx.Graph(rdmolops.GetAdjacencyMatrix(MolFromSmiles(smiles_rdkit[ i ]))))
    if len(cycle_list) == 0:
        cycle_length = 0
    else:
        cycle_length = max([ len(j) for j in cycle_list ])
    if cycle_length <= 6:
        cycle_length = 0
    else:
        cycle_length = cycle_length - 6
    cycle_scores.append(-cycle_length)

SA_scores_normalized = (np.array(SA_scores) - np.mean(SA_scores)) / np.std(SA_scores)
SA_scores_normalized = SA_scores_normalized.reshape((-1,1))
cycle_scores_normalized = (np.array(cycle_scores) - np.mean(cycle_scores)) / np.std(cycle_scores)
cycle_scores_normalized = cycle_scores_normalized.reshape((-1,1))

latent_points = []
for i in xrange(0, len(smiles), batch_size):
    batch = smiles[i:i+batch_size]
    mol_vec = model.encode_latent_mean(batch)
    latent_points.append(mol_vec.data.cpu().numpy())

# We store the results
latent_points = np.vstack(latent_points)
np.save('latent_means.npy', latent_points)

logKas = np.load('../data/zinc/logKas.npy')
targets = SA_scores_normalized + logKas + cycle_scores_normalized
np.save('../data/zinc/targets.npy', targets)
np.save('../data/zinc/SA_scores.npy', np.array(SA_scores))
np.save('../data/zinc/cycle_scores.npy', np.array(cycle_scores))
