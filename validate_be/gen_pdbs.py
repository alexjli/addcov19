from rdkit import Chem
from rdkit.Chem import AllChem
import os

if not os.path.exists("lig_pdbs"):
    os.mkdir("lig_pdbs") 

with open("bo_results_unique_smiles.txt") as fp:
    smiles = [line.strip() for line in fp]

for idx, smile in enumerate(smiles):
    print idx, smile
    m = Chem.MolFromSmiles(smile)
    m = Chem.AddHs(m)
    AllChem.EmbedMolecule(m)
    AllChem.UFFOptimizeMolecule(m)
    Chem.MolToPDBFile(m, 'lig_pdbs/lig%d.pdb' % idx)
