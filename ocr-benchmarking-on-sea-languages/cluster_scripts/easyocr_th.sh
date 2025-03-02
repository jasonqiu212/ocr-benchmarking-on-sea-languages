#!/bin/bash
#SBATCH --time=999
#SBATCH --job-name=easyocr_th
#SBATCH --gpus=1
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=jason.qiu@u.nus.edu

source sample/bin/activate
python3 easyocr_th.py
deactivate
