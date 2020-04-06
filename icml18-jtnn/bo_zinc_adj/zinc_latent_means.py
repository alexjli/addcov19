import torch
import torch.nn as nn
from torch.autograd import Variable
from optparse import OptionParser
import traceback


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

batch_size = 1
hidden_size = int(opts.hidden_size)
latent_size = int(opts.latent_size)
depth = int(opts.depth)

model = JTNNVAE(vocab, hidden_size, latent_size, depth)
model.load_state_dict(torch.load(opts.model_path))
model = model.cuda()

logKas = np.load('../../data/zinc/logKas.npy')
logKas_tryp = np.load('../../data/zinc/logKas_tryp.npy')

idx = []


print "gen smiles"
smiles_rdkit = []
for i in xrange(len(smiles)):
    try:
        smiles_rdkit.append(MolToSmiles(MolFromSmiles(smiles[ i ]), isomericSmiles=True))
        idx.append(i)
    except:
        smiles_rdkit.append(None)

print "gen sa"
SA_scores = []
for i in xrange(len(smiles)):
    if smiles_rdkit[i] is None:
        SA_scores.append(0)
        continue
    SA_scores.append(-sascorer.calculateScore(MolFromSmiles(smiles_rdkit[ i ])))

import networkx as nx


print "gen cycle score"
cycle_scores = []
for i in range(len(smiles)):
    if smiles_rdkit[i] is None:
        cycle_scores.append(0)
        continue
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

errors = []
print "gen latent means"
latent_points = []
for i in xrange(0, len(smiles)):
    batch = []
    if i in idx:
        batch.append(smiles[i])
    else:
        continue
        print(i)
    try:
        mol_vec = model.encode_latent_mean(batch)
        latent_points.append(mol_vec.data.cpu().numpy())
    except Exception as e:
        print(i)
        print smiles[i]
        traceback.print_exc()
        errors.append(i)

logKas_list = logKas.reshape((-1,)).tolist()
logKas_tryp_list = logKas_tryp.reshape((-1,)).tolist()
for i in xrange(29999,-1,-1):
    if i not in idx:
        pos = i
        del SA_scores[pos]
        del cycle_scores[pos]
        del logKas_list[pos]
        del logKas_tryp_list[pos]

    elif i in errors:
        pos = idx.index(i)
        del idx[pos]
        del SA_scores[pos]
        del cycle_scores[pos]
        del logKas_list[pos]
        del logKas_tryp_list[pos]


# We store the results
latent_points = np.vstack(latent_points)
np.save('../../data/zinc/latent_means.npy', latent_points)
np.save('../../data/zinc/idx.npy', np.array(idx).reshape((-1,1)))
np.save('../../data/zinc/logKas_trimmed.npy', np.array(logKas_list).reshape((-1,1)))
np.save('../../data/zinc/logKas_tryp_trimmed.npy', np.array(logKas_tryp_list).reshape((-1,1)))


SA_scores_normalized = (np.array(SA_scores) - np.mean(SA_scores)) / np.std(SA_scores)
SA_scores_normalized = SA_scores_normalized.reshape((-1,1))
cycle_scores_normalized = (np.array(cycle_scores) - np.mean(cycle_scores)) / np.std(cycle_scores)
cycle_scores_normalized = cycle_scores_normalized.reshape((-1,1))


targets = SA_scores_normalized + np.array(logKas_list).reshape((-1,1)) + cycle_scores_normalized
np.save('../../data/zinc/targets.npy', targets)
np.save('../../data/zinc/SA_scores.npy', np.array(SA_scores).reshape((-1,1)))
np.save('../../data/zinc/cycle_scores.npy', np.array(cycle_scores).reshape((-1,1)))
