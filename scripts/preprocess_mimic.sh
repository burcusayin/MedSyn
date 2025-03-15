#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem-per-cpu=4096
#SBATCH -N 1
#SBATCH --error=/home/error/preprocess_mimic.err
#SBATCH --output=/home/output/output.txt


python src.preprocess_mimicIV.py \
--mimic4_root /home/dataset/mimiciv/3.1/ \
--mimic4_note_root /home/dataset/mimic-iv-note/2.2/note/ \
--output_file_with_icd9 /home/dataset/mimiciv/3.1/preprocessed/mimicIV_icd9 \
--output_file_with_icd10 /home/dataset/mimiciv/3.1/preprocessed/mimicIV_icd10

