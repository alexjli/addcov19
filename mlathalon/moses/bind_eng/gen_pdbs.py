from rdkit import Chem
from rdkit.Chem import AllChem

with open("mol_samples.txt") as fp:
	smiles = [line.strip() for line in fp]

for idx, smile in enumerate(smiles):
	m = Chem.MolFromSmiles(smile)
	m = Chem.AddHs(m)
	AllChem.EmbedMolecule(m)
	AllChem.UFFOptimizeMolecule(m)
	Chem.MolToPDBFile(m, 'lig_pdbs/%d.pdb' % idx)
