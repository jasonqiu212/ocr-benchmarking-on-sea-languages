#!/bin/bash
#SBATCH --time=999
#SBATCH --job-name=finetune_got_th
#SBATCH --gpus=1
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=jason.qiu@u.nus.edu

source sample/bin/activate
python3 finetune_got_th.py
deactivate
