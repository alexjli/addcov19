import os
import math
import numpy as np

def oom(units):
    if units == 'pM':
        return -12
    elif units == 'nM':
        return -9
    elif units == 'uM':
        return -6
    elif units == 'mM':
        return -3
    else:
        raise Exception("Invalid input")

vals = []
lig_val = []


for i in range(0,30000):
    path = "bind_eng/nnscores/lig%d_out.log" % i
    name = "lig%d" % i
    last = os.popen("tail -n 1 %s" % path).read()
    last = last.split()
    print(last)
    logKa = - (math.log10(float(last[0])) + oom(last[1]))
    vals.append(logKa)
    print(i, logKa)
    lig_val.append((i, logKa))

arr = np.array(vals).reshape(30000,1)
np.save("logKas.npy",arr)
lig_val.sort(key=lambda x: x[1], reverse=True)
print lig_val[:10]