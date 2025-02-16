#!/bin/bash
#SBATCH --time=999
#SBATCH --job-name=tesseract_en
#SBATCH --gpus=1
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=jason.qiu@u.nus.edu

source ~/miniconda3/bin/activate
conda activate sample
python3 tesseract_en.py
conda deactivate
