#!/bin/bash
module load python/3.7

srun --mem 20GB python "$@"