#!/bin/bash
#SBATCH -t 2:00:00

module load openmind/singularity
singularity run ../mlathalon.simg ./nnscore.sh
