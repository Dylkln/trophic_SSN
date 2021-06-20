#!/bin/bash
#
#SBATCH --partition=long
#SBATCH --mem=200GB
#SBATCH --mail-user=klein.dylan@outlook.com
#SBATCH --mail-type=ALL

module load diamond/0.9.36

srun  diamond blastp -d metdb_dia_db.dmnd -q cat_tr.fasta -o metdb_ssn -e 1e-5 --sensitive -f 6 qseqid qlen qstart qend sseqid slen sstart send length pident ppos score evalue bitscore
