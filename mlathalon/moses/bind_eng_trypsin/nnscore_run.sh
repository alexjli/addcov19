#!/bin/bash
#SBATCH -t 6:00:00
#SBATCH --array=0-11 

module load openmind/singularity
singularity run mlathalon.simg ./nnscore.sh $SLURM_ARRAY_TASK_ID
