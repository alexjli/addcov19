import json
import numpy as np

logKas = np.load('logKas.npy')
with open('bo_results_unique_smiles.txt') as fp:
	smiles = [line.strip() for line in fp]

smiles_scores = {smile: val for smile, val in zip(smiles, logKas.tolist())}

json.dump(smiles_scores, open('smiles_scores.json', 'w'))
