import rdkit
from rdkit.Chem import Descriptors
from rdkit.Chem import MolFromSmiles, MolToSmiles
from rdkit.Chem import rdmolops
import sascorer

import numpy as np

with open("../fast_molvae/mol_samples.txt") as fp:
    smiles = [line.strip() for line in fp]


logKas = np.load('../../data/logKas.npy')

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

targets = SA_scores_normalized + logKas + cycle_scores_normalized
np.save('../../data/targets.npy', targets)
np.save('../../data/SA_scores.npy', np.array(SA_scores))
np.save('../../data/cycle_scores.npy', np.array(cycle_scores))
