#!/bin/bash
#SBATCH -t 12:00:00
#SBATCH -N 1
#SBATCH -n 40
#SBATCH --gres=gpu
#SBATCH --array=1-10

module load openmind/singularity
singularity run --nv bo_ext2.simg ./rbomd.sh $SLURM_ARRAY_TASK_ID
