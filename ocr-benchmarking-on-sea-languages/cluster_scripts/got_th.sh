#!/bin/bash
#SBATCH --time=7199
#SBATCH --job-name=got_th
#SBATCH --gpus=1
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=jason.qiu@u.nus.edu

source sample/bin/activate
python3 got_th.py
deactivate
