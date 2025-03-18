#!/bin/bash
#SBATCH --time=7199
#SBATCH --job-name=finetune_got_th
#SBATCH --gpus=4
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=jason.qiu@u.nus.edu

source sample/bin/activate

NPROC_PER_NODE=4 \
CUDA_VISIBLE_DEVICES=0,1,2,3 \
swift sft \
    --model_type got-ocr2 \
    --model_id_or_path stepfun-ai/GOT-OCR2_0 \
    --sft_type lora \
    --dataset ../finetuning/thai-dataset.json \
    --deepspeed default-zero2

deactivate
