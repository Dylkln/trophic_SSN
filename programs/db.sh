#!/bin/bash
#
#SBATCH --partition=long
#SBATCH --mem=50GB
#SBATCH --mail-user=klein.dylan@outlook.com
#SBATCH --mail-type=ALL

module load diamond/0.9.36
srun  diamond makedb --in cat_tr.fasta --db metdb_dia_db
