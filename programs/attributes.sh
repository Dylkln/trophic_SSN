#!/bin/bash
#
#SBATCH --partition=long
#SBATCH --mem=4GB
#SBATCH --mail-user=klein.dylan@outlook.com
#SBATCH --mail-type=ALL
#SBATCH --array=0-461

module load python/3.7

INPUTS=(../results/records/*)

srun python attributes.py -s ${INPUTS[$SLURM_ARRAY_TASK_ID]} -a ../data/an_files.txt -t ../data/metdb_full_count_transcript_final.csv
