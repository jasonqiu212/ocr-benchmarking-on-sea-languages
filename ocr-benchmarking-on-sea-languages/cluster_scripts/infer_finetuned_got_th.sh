#!/bin/bash
#SBATCH --time=7199
#SBATCH --job-name=infer_finetuned_got_th
#SBATCH --gpus=1
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=jason.qiu@u.nus.edu

source sample/bin/activate

CUDA_VISIBLE_DEVICES=0 swift infer \
    --model output/GOT-OCR2_0/v1-20250318-235123/checkpoint-1071 \
    --infer_backend pt \
    --max_batch_size 1 \
    --load_data_args true

deactivate
