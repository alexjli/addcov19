#!/bin/bash
#SBATCH -t 12:00:00
#SBATCH -n 30
#SBATCH --gres=gpu:1

module load openmind/singularity
time singularity run bo_ext_local.simg ./bomdar.sh 1
