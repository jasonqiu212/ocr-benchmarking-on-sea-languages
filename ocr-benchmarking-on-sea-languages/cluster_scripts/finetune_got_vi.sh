#!/bin/bash
#SBATCH --time=7199
#SBATCH --job-name=finetune_got_vi
#SBATCH --gpus=1
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=jason.qiu@u.nus.edu

source sample/bin/activate

# CUDA_VISIBLE_DEVICES=0 swift sft \
#     --model stepfun-ai/GOT-OCR2_0 \
#     --dataset ../finetuning/datasets/vietnamese-dataset-500.json \
#     --split_dataset_ratio 0.2

CUDA_VISIBLE_DEVICES=0 swift sft \
    --model stepfun-ai/GOT-OCR2_0 \
    --dataset ../finetuning/datasets/vietnamese/vietnamese-train-dataset-50.json \
    --split_dataset_ratio 0

deactivate
