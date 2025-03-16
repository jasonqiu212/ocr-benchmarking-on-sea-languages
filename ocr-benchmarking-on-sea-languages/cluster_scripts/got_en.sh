#!/bin/bash
#SBATCH --time=999
#SBATCH --job-name=got_en
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=jason.qiu@u.nus.edu

source sample/bin/activate
python3 got_en.py
deactivate
