#!/bin/bash
#SBATCH -t 3:00:00
#SBATCH -N 1
#SBATCH -n 40

module load openmind/singularity
singularity run ../mlathalon.simg ./vina_screen.sh

