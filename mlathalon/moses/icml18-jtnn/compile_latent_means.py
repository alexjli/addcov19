import numpy as np

arrs = []

for i in xrange(60):
    arrs.append(np.load('latent_means/latent_means_%d.npy' % i))

full = np.concatenate(arrs)
np.save('latent_means/latent_means.npy', full)
