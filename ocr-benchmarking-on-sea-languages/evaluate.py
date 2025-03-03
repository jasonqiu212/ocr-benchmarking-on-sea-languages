"""This file provides operations to evaluate OCR performance."""

import csv
import os

import jiwer
from tqdm import tqdm


def evaluate_to_csv(source_path: str, target_file_name: str, prediction_file_name: str, output_file_name: str):
    data = [['Article Name', 'CER', 'WER']]
    sorted_articles = sorted(os.listdir(source_path))

    for article in tqdm(sorted_articles):
        target_file_path = f'{source_path}/{article}/{target_file_name}'
        prediction_file_path = f'{source_path}/{article}/{prediction_file_name}'

        if os.path.exists(prediction_file_path) and os.path.exists(target_file_path):
            target_text = open(target_file_path, 'r').read()
            prediction_text = open(prediction_file_path, 'r').read()

            cer = jiwer.cer(target_text, prediction_text)
            wer = jiwer.wer(target_text, prediction_text)

            formatted_cer = round(cer, 4)
            formatted_wer = round(wer, 4)
            data.append([article, formatted_cer, formatted_wer])
        else:
            print(f'{article} does not have results')

    with open(f'{source_path}/{output_file_name}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
