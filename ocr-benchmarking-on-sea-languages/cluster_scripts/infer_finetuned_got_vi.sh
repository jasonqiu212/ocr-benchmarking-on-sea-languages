#!/bin/bash
#SBATCH --time=7199
#SBATCH --job-name=infer_finetuned_got_vi
#SBATCH --gpus=1
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=jason.qiu@u.nus.edu

source sample/bin/activate

CUDA_VISIBLE_DEVICES=0 swift infer \
    --adapters output/GOT-OCR2_0/v0-20250319-105430/checkpoint-1212 \
    --infer_backend pt \
    --max_batch_size 1 \
    --load_data_args true

deactivate
