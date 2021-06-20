#!/bin/bash
#
#SBATCH --partition=long
#SBATCH --mem=20GB
#SBATCH --mail-user=klein.dylan@outlook.com
#SBATCH --mail-type=ALL

srun  cat transdecoder_file_names.txt | xargs cat > cat_tr.txt