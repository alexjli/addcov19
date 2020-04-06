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
    scores_6LU7 = []
    scores_1h4w = []

    # making directories if they don't exist -- saves the hassle of doing them in script
    if not os.path.exists("lig_pdbs"):
        os.mkdir("lig_pdbs")
    if not os.path.exists("lig_pdbqts"):
        os.mkdir("lig_pdbqts")
    if not os.path.exists("vina_dockings"):
        os.mkdir("vina_dockings")
    if not os.path.exists("nnscores"):
        os.mkdir("nnscores")

    # make pdbs
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
        path = "nnscores/iter" + str(iteration) + "lig%d_out_6LU7.log" % i # this isn't going to work -- change the names
        name = "iter" + str(iteration) + "lig%d" % i # this isn't going to  work either -- change the names
        last = os.popen("tail -n 1 %s" % path).read()
        last = last.split()
        logKa = - (math.log10(float(last[0])) + oom(last[1]))
        scores_6LU7.append(logKa)

    
    for i in xrange(50):
        path = "nnscores/iter" + str(iteration) + "lig%d_out_1h4w.log" % i # this isn't going to work -- change the names
        name = "iter" + str(iteration) + "lig%d" % i # this isn't going to  work either -- change the names
        last = os.popen("tail -n 1 %s" % path).read()
        last = last.split()
        logKa = - (math.log10(float(last[0])) + oom(last[1]))
        scores_1h4w.append(logKa)

    return scores_6LU7, scores_1h4w
    

## /Additions

with open('temp_mol_samples.txt') as fp:
	smiles = [line.strip() for line in fp]

sample = smiles[:10]
scores1, scores2 = get_scores(sample, 1)
print scores1
print
print scores2
