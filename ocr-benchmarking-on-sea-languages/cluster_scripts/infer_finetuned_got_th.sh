#!/bin/bash
#SBATCH --time=7199
#SBATCH --job-name=infer_finetuned_got_th
#SBATCH --gpus=1
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=jason.qiu@u.nus.edu

source sample/bin/activate

CUDA_VISIBLE_DEVICES=0 swift infer \
    --ckpt_dir output/got-ocr2/v1-20250318-235123/checkpoint-1071 \
    --load_dataset_config true \

deactivate
