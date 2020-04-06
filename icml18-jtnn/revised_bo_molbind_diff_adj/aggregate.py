import rdkit
from rdkit import Chem
from rdkit.Chem import MolFromSmiles, MolToSmiles
from rdkit.Chem import Descriptors
import math
import json
import numpy as np

import sascorer
import networkx as nx
from rdkit.Chem import rdmolops

lg = rdkit.RDLogger.logger() 
lg.setLevel(rdkit.RDLogger.CRITICAL)

SA_scores = np.load('data/moses/SA_scores.npy')
cycle_scores = np.load('data/moses/cycle_scores.npy')

# We define the functions used to load objects
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

def get_smiles(seed, iteration, index):
    m = Chem.MolFromPDBFile("lig_pdbs{}/iter{}lig{}.pdb".format(seed, iteration, index))
    return Chem.MolToSmiles(m, isomericSmiles=False)

def get_logKa(seed, iteration, index, protein_name):
    fname = "nnscores{}/iter{}lig{}_out_".format(seed, iteration, index, protein_name) + protein_name + ".log"
    with open(fname, "r") as f:
        last_line = f.readlines()[-1]
    last_line = last_line.split()
    try:
        logKa = - (math.log10(float(last_line[0])) + oom(last_line[1]))
    except:
        print("AAAAAAAAA")
        logKa = None
    return logKa

def get_SA_and_cycle_score(curr_smiles):
    curr_mol = MolFromSmiles(curr_smiles)
    current_SA_score = -sascorer.calculateScore(curr_mol)

    cycle_list = nx.cycle_basis(nx.Graph(rdmolops.GetAdjacencyMatrix(curr_mol)))
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

    return current_SA_score, current_SA_score_normalized, current_cycle_score, current_cycle_score_normalized

def get_results_dict():
    results_dict = {}
    for seed in xrange(1, 11):
        for iteration in xrange(0, 5):
            for index in xrange(0, 50):
                curr_seed = seed
                curr_iteration = iteration
                curr_index = index
                curr_smiles = get_smiles(curr_seed, curr_iteration, curr_index)

                curr_entry = curr_smiles

                curr_1h4w_logKa = get_logKa(curr_seed, curr_iteration, curr_index, "1h4w")
                curr_6LU7_logKa = get_logKa(curr_seed, curr_iteration, curr_index, "6LU7")

                ## calculating other stuff
                current_SA_score, current_SA_score_normalized, current_cycle_score, current_cycle_score_normalized = get_SA_and_cycle_score(curr_smiles)

                curr_data = (curr_seed, curr_iteration, curr_index, curr_1h4w_logKa, curr_6LU7_logKa, current_SA_score, current_SA_score_normalized, current_cycle_score, current_cycle_score_normalized)

                results_dict[curr_entry] = curr_data
    return results_dict

now_this_is_epic = get_results_dict()

# keys are smiles
# entries are
    # seed
    # iteration
    # index
    # 1h4w logKa
    # 6LU7 logKa

with open("aggregate_results.json", "w") as f:
    json.dump(now_this_is_epic, f)
