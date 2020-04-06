#!/bin/bash

conda init bash
conda activate jtnn_env
export PYTHONPATH=$PWD
pwd
cd bo_molbind_diff_adj_revised
python test_pipeline.py
