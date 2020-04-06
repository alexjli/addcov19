import json

def avg(l):
	return sum(l)/len(l)

later_print = []
with open('../revised_results.json') as fp:
	revised_results = json.load(fp)

validates = ['vanilla.json', 'adj.json', 'diff.json', 'diff_adj.json']

for raw in validates:
	print raw
	current_dict = None
        if raw == validates[0]:
		current_dict = revised_results['revised_bo_molbind']
	elif raw == validates[1]:
		current_dict = revised_results['revised_bo_molbind_adj']
	elif raw == validates[2]:
		current_dict = revised_results['revised_bo_molbind_diff']
	else:
		current_dict = revised_results['revised_bo_molbind_diff_adj']

	with open(raw) as fp:
		smiles_dict = json.load(fp)
	pairs = [[smiles, val] for smiles, val in smiles_dict.items()]
	f = filter(lambda x: x[1][3] < 6 and x[1][4] > 8, pairs)
	f.sort(key = lambda x: x[1][4] - x[1][3])
	for data in f:
		print data
	print
	print "list for future use if needed"
	print f
	print
	
