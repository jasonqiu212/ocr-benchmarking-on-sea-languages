#!/bin/bash
#SBATCH --time=999
#SBATCH --job-name=tesseract_vi
#SBATCH --gpus=1
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=jason.qiu@u.nus.edu

source sample/bin/activate
python3 tesseract_vi.py
deactivate
