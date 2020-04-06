import json

fname = "bo_results.temp"
all_smiles_dicts = []
curr_smiles_dict = {}

# gathering smiles_dicts from all the directories
with open(fname) as f:
    for line in f:
        curr_line = line.split()

        # looking to see if the new line indicates a new directory
        if len(curr_line) == 0:
            pass
        elif len(curr_line) == 1:
            curr_smiles_dict = {"name" : curr_line[0]}
            all_smiles_dicts.append(curr_smiles_dict)

        elif len(curr_line) == 2:
            smiles = curr_line[0]
            binding_aff = curr_line[1]
            if smiles in curr_smiles_dict:
                curr_smiles_dict[smiles].append(binding_aff)
            else:
                curr_smiles_dict[smiles] = [binding_aff]
        else:
            raise ValueError

# computing unique smiles
outputfname_1 = "bo_results_unique_smiles_zinc.txt"
with open(outputfname_1, 'w') as f:
    # compute string here
    list_of_smile_sets = [ set(smiles_dict.keys()) for smiles_dict in all_smiles_dicts ]
    all_smiles = set.union(*list_of_smile_sets)
    all_smiles.remove('name')

    for smiles in all_smiles:
        writestring = smiles
        f.write(writestring + "\n")

# dumping json

# first we move around some stuff
all_smiles_dicts_json_dump = {}
for smiles_dict in all_smiles_dicts:
    curr_dict_name = smiles_dict.pop("name")

    # processing curr_dict_name to be the name of the directory
    curr_dict_name = curr_dict_name[curr_dict_name.index("bo_"):]

    all_smiles_dicts_json_dump[curr_dict_name] = smiles_dict

outputfname_2 = "bo_results_zinc.json"
with open(outputfname_2, 'w') as f:
    json.dump(all_smiles_dicts_json_dump, f)
