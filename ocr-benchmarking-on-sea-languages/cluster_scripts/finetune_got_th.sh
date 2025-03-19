#!/bin/bash
#SBATCH --time=7199
#SBATCH --job-name=finetune_got_th
#SBATCH --gpus=1
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=jason.qiu@u.nus.edu

source sample/bin/activate

CUDA_VISIBLE_DEVICES=0 swift sft \
    --model stepfun-ai/GOT-OCR2_0 \
    --dataset ../finetuning/thai-dataset.json \
    --split_dataset_ratio 0.2

deactivate
