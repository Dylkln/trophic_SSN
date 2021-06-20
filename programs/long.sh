#!/bin/bash
#
#SBATCH --partition=long
#SBATCH --mem=40GB
#SBATCH --mail-user=klein.dylan@outlook.com
#SBATCH --mail-type=ALL

module load python/3.7

srun python "$@"