#!/bin/sh
#SBATCH --job-name=run_tesseract
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=jason.qiu@u.nus.edu
#SBATCH --gpus=1

python3 run_tesseract.py
