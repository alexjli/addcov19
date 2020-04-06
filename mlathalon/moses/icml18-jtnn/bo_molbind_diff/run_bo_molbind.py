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
y1 = -np.load('../../data/logKas.npy')
y = y1 - y2
y = y.reshape((-1, 1))

print y

n = X.shape[ 0 ]
permutation = np.random.choice(n, n, replace = False)

X_train = X[ permutation, : ][ 0 : np.int(np.round(0.9 * n)), : ]
X_test = X[ permutation, : ][ np.int(np.round(0.9 * n)) :, : ]

y_train = y[ permutation ][ 0 : np.int(np.round(0.9 * n)) ]
y_test = y[ permutation ][ np.int(np.round(0.9 * n)) : ]

np.random.seed(random_seed)

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
        tree_vec,mol_vec = np.hsplit(all_vec, 2)
        tree_vec = create_var(torch.from_numpy(tree_vec).float())
        mol_vec = create_var(torch.from_numpy(mol_vec).float())
        s = model.decode(tree_vec, mol_vec, prob_decode=False)
        if s is not None: 
            valid_smiles.append(s)
            new_features.append(all_vec)
    
    print len(valid_smiles), "molecules are found"
    valid_smiles = valid_smiles[:50]
    new_features = next_inputs[:50]
    new_features = np.vstack(new_features)
    save_object(valid_smiles, args.save_dir + "/valid_smiles{}.dat".format(iteration))

    import sascorer
    import networkx as nx
    from rdkit.Chem import rdmolops

    pred, uncert = sgp.predict(new_features, 0* new_features)
    print pred.shape
    print pred
    scores = [score[0] for score in pred]

    print valid_smiles
    print scores

    save_object(scores, args.save_dir + "/scores{}.dat".format(iteration))
    
    if len(new_features) > 0:
        X_train = np.concatenate([ X_train, new_features ], 0)
        y_train = np.concatenate([ y_train, np.array(scores)[ :, None ] ], 0)
    

    iteration += 1
