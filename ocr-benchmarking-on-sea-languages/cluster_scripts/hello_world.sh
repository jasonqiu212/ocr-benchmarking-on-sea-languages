#!/bin/sh
#SBATCH --time=999
#SBATCH --job-name=hello_world
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=jason.qiu@u.nus.edu

python3 hello_world.py
