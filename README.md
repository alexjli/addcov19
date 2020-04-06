# ADD-COV-19: Automated Drug Discovery for SARS-like Coronavirus 2

Herein is our codedump for our project ADD-COV-19, an automated drug discovery pipeline to discovery small molecule inhibitors for SARS-COV-2. This project was done for MIT MIC's ML-athon 2020.

Our README is in the process of being fully completed! Please check in in a bit for the complete README.

## Software dependencies

This software depends on a few packages:
* [JTNNVAE](https://arxiv.org/abs/1802.04364), used for molecular VAE
* [GrammarVAE](https://arxiv.org/abs/1703.01925), in particular the custom Theano package used for BO optimization
* [Autodock Vina](http://vina.scripps.edu/), a docking software that supports multithreading
* [MGLTools](http://mgltools.scripps.edu/), a subset of AutodockTools used for molecular representation preprocessing
* [NNScore2](https://pubs.acs.org/doi/10.1021/ci2003889), a neural net scoring function for ligand-protein binding

## Included Code

Unfortunately, our code base is somewhat of a mess right now. We combined all our various working directories across machines, but didn't have time to clean it up before uploading. Additionally, we had to scrub our data from our folders before uploading to Github, as the original folder in its entirety was roughly 100Gb. While we hope to clean the code up soon, here's a high level overview of the kinds of folders you'll find:

* bind_eng: a folder that generally was used to compute training data ligand PDBs, PDBQTs, dockings, and scorings for protein 6LU7
* bind_eng_trypsin: a folder that generally did the same thing as bind_eng, but for protein 1h4w
* data: contains training data, as well as other data such as vocabularies for JTNNs
* validate_be, validate_be_tryp: reminant folders used to validate our first rounds of BO
* grammarVAE: used for custom Theano package
* MGLTools: used for MGLTools scripts
* icml18-jtnn: contains JTNNVAE code, as well as our BO optimizations
	- bo_molbind_*: a first round of BO optimizations that had a flaw in its algorithm but produced decent results. Not reported in the Medium article due to the flaw it contained, but retained for its potential future usage.
	- revised_bo_molbind*: BO optimization with a correct algorithm. Results are stored in revised_bo_molbind_results
* anything that contains the word zinc: a trial of using our model trained on the ZINC dataset rather than MOSES. We weren't able to finish the work, but it's also retained for its potential future usage.
