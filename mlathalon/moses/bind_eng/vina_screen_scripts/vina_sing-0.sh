#!/bin/bash
#SBATCH -n 40
#SBATCH -t 11:00:00
#SBATCH --gres=gpu

module load openmind/singularity
pwd
singularity run --nv mlathalon.simg ./vina_screen-0.sh