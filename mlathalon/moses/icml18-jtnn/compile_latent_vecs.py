import numpy as np

arrs = []

for i in xrange(60):
    arrs.append(np.load('latent_vecs/latent_vecs_%d.npy' % i))

full = np.concatenate(arrs)
np.save('latent_vecs/latent_vecs.npy', full)
