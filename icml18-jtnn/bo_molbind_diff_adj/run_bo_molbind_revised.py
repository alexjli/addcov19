import pickle
import gzip
from sparse_gp import SparseGP
import scipy.stats as sps
import numpy as np
import os.path

import rdkit
from rdkit.Chem import MolFromSmiles, MolToSmiles
from rdkit.Chem import Descriptors

import torch
import torch.nn as nn
from fast_jtnn import *

import argparse

lg = rdkit.RDLogger.logger() 
lg.setLevel(rdkit.RDLogger.CRITICAL)

# We define the functions used to load and save objects
def save_object(obj, filename):
    result = pickle.dumps(obj)
    with gzip.GzipFile(filename, 'wb') as dest: dest.write(result)
    dest.close()

def load_object(filename):
    with gzip.GzipFile(filename, 'rb') as source: result = source.read()
    ret = pickle.loads(result)
    source.close()
    return ret

## Additions

from rdkit import Chem
from rdkit.Chem import AllChem
import os
import math
import subprocess

def oom(units):
    if units == "fM":
        return -15
    if units == "pM":
        return -12
    if units == "nM":
        return -9
    if units == "uM":
        return -6
    if units == "mM":
        return -3
    if units == "M":
        return 0
    else:
        raise ValueError("invalid input")

def get_scores(valid_smiles, iteration):
    scores = []

    # making directories if they don't exist -- saves the hassle of doing them in script
    if not os.path.exists("lig_pdbs"):
        os.mkdir("lig_pdbs")
    if not os.path.exists("lig_pdbqts"):
        os.mkdir("lig_pdbqts")
    if not os.path.exists("vina_dockings"):
        os.mkdir("vina_dockings")
    if not os.path.exists("nnscores"):
        os.mkdir("nnscores")

    # make pdbqs
    for index, smile in enumerate(valid_smiles):
        print "Calculating scores for iteration " + str(iteration)
        m = Chem.MolFromSmiles(smile)
        m = Chem.AddHs(m)
        AllChem.EmbedMolecule(m)
        AllChem.UFFOptimizeMolecule(m)
        Chem.MolToPDBFile(m, "lig_pdbs/iter" + str(iteration) + "lig%d.pdb" % index)

    # populate nnscores
    subprocess.call(["./get_scores.sh", str(iteration)])

    # get logKas from nnscores
    # idk what to call the files so here we go
    for i in xrange(50):
        path = "nnscores/iter" + str(iteration) + "lig%d_out.log" % i # this isn't going to work -- change the names
        name = "iter" + str(iteration) + "lig%d" % i # this isn't going to  work either -- change the names
        last = os.popen("tail -n 1 %s" % path).read()
        last = last.split()
        logKa = - (math.log10(float(last[0])) + oom(last[1]))
        scores.append(logKa)

    return scores
    
## /Additions


parser = argparse.ArgumentParser()
parser.add_argument('--vocab', required=True)
parser.add_argument('--model', required=True)

parser.add_argument('--hidden_size', type=int, default=450)
parser.add_argument('--latent_size', type=int, default=56)
parser.add_argument('--depthT', type=int, default=20)
parser.add_argument('--depthG', type=int, default=3)
parser.add_argument("--seed", type=int, default=None)
parser.add_argument('--save_dir')
args = parser.parse_args()

vocab = [x.strip("\r\n ") for x in open(args.vocab)] 
vocab = Vocab(vocab)

random_seed = int(args.seed)

model = JTNNVAE(vocab, args.hidden_size, args.latent_size, args.depthT, args.depthG)
model.load_state_dict(torch.load(args.model))
model = model.cuda()



# We load the random seed
np.random.seed(random_seed)

# We load the data (y is minued!)
X = np.load('../../data/latent_means.npy')
y2 = -np.load('../../data/logKas_tryp.npy')
y1 = -np.load('../../data/targets.npy')
y = y1 - y2
y = y.reshape((-1, 1))

n = X.shape[ 0 ]
permutation = np.random.choice(n, n, replace = False)

X_train = X[ permutation, : ][ 0 : np.int(np.round(0.9 * n)), : ]
X_test = X[ permutation, : ][ np.int(np.round(0.9 * n)) :, : ]

y_train = y[ permutation ][ 0 : np.int(np.round(0.9 * n)) ]
y_test = y[ permutation ][ np.int(np.round(0.9 * n)) : ]

np.random.seed(random_seed)

SA_scores = np.load('../../data/SA_scores.npy')
cycle_scores = np.load('../../data/cycle_scores.npy')

iteration = 0
while iteration < 5:
    # We fit the GP
    np.random.seed(iteration * random_seed)
    M = 500
    sgp = SparseGP(X_train, 0 * X_train, y_train, M)
    sgp.train_via_ADAM(X_train, 0 * X_train, y_train, X_test, X_test * 0, y_test, minibatch_size = 10 * M, max_iterations = 100, learning_rate = 0.001)

    pred, uncert = sgp.predict(X_test, 0 * X_test)
    error = np.sqrt(np.mean((pred - y_test)**2))
    testll = np.mean(sps.norm.logpdf(pred - y_test, scale = np.sqrt(uncert)))
    print 'Test RMSE: ', error
    print 'Test ll: ', testll

    pred, uncert = sgp.predict(X_train, 0 * X_train)
    error = np.sqrt(np.mean((pred - y_train)**2))
    trainll = np.mean(sps.norm.logpdf(pred - y_train, scale = np.sqrt(uncert)))
    print 'Train RMSE: ', error
    print 'Train ll: ', trainll

    # We pick the next 60 inputs
    next_inputs = sgp.batched_greedy_ei(60, np.min(X_train, 0), np.max(X_train, 0))

    valid_smiles = []
    new_features = []

    for i in xrange(60):
        all_vec = next_inputs[i].reshape((1,-1))
        tree_vec, mol_vec = np.hsplit(all_vec, 2)
        tree_vec = create_var(torch.from_numpy(tree_vec).float())
        mol_vec = create_var(torch.from_numpy(mol_vec).float())
        s = model.decode(tree_vec, mol_vec, prob_decode=False)
        if s is not None: 
            valid_smiles.append(s)
            new_features.append(all_vec)
    
    print len(valid_smiles), "molecules are found"

    valid_smiles = valid_smiles[:50]

    # I think this is a bug? not sure though -- for now let's keep it the original way
    # new_features = next_inputs[:50]
    new_features = new_features[:50]

    # we don't need this line anymore because we're using a better function
    # new_features = np.vstack(new_features)
    
    # temporarily disabled because I'm scared of changing things
    # save_object(valid_smiles, args.save_dir + "/valid_smiles{}.dat".format(iteration))

    print valid_smiles

    import sascorer
    import networkx as nx
    from rdkit.Chem import rdmolops

    # pred, uncert = sgp.predict(new_features, 0* new_features)
    # print pred.shape
    # scores = [score[0] for score in pred]
    # print scores

    scores = get_scores(valid_smiles, iteration)



    for i in range(len(valid_smiles)):
        current_SA_score = -sascorer.calculateScore(MolFromSmiles(valid_smiles[ i ]))
        cycle_list = nx.cycle_basis(nx.Graph(rdmolops.GetAdjacencyMatrix(MolFromSmiles(valid_smiles[ i ]))))
        if len(cycle_list) == 0:
            cycle_length = 0
        else:
            cycle_length = max([ len(j) for j in cycle_list ])
        if cycle_length <= 6:
            cycle_length = 0
        else:
            cycle_length = cycle_length - 6

        current_cycle_score = -cycle_length

        current_SA_score_normalized = (current_SA_score - np.mean(SA_scores)) / np.std(SA_scores)
        current_cycle_score_normalized = (current_cycle_score - np.mean(cycle_scores)) / np.std(cycle_scores)

        scores[i] -= current_SA_score_normalized + current_cycle_score_normalized

    print scores

    save_object(scores, args.save_dir + "/scores{}.dat".format(iteration))
    
    if len(new_features) > 0:
        X_train = np.concatenate([ X_train, new_features ], 0)
        y_train = np.concatenate([ y_train, np.array(scores)[ :, None ] ], 0)
    
    iteration += 1
