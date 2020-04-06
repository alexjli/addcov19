#!/bin/bash
#SBATCH -t 6:00:00
#SBATCH -n 40
#SBATCH -N 1

module load openmind/singularity
singularity run mlathalon.simg ./vina_screenx.sh
