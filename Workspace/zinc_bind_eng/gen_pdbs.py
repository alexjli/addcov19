from rdkit import Chem
from rdkit.Chem import AllChem
import os

if not os.path.exists("lig_pdbs"):
    os.mkdir("lig_pdbs") 

with open("mol_samples.txt") as fp:
    smiles = [line.strip() for line in fp]

for idx, smile in enumerate(smiles):
    try:
        m = Chem.MolFromSmiles(smile)
        m = Chem.AddHs(m)
        AllChem.EmbedMolecule(m)
        AllChem.UFFOptimizeMolecule(m)
        Chem.MolToPDBFile(m, 'lig_pdbs/lig%d.pdb' % idx)
    except Exception as e:
        print smile
        print e
