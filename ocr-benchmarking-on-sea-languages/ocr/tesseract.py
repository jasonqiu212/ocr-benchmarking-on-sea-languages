import os
import time
from typing import List

import pytesseract


def run_tesseract_on_all(source_path: str, language: str):
    """
    Runs Tesseract on all articles in a directory and stores results in an output file.

    Args:
        source_path: Path to articles
        language: Tesseract language code to detect. List of Tesseract language codes be found at: https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html.
    """
    print(f'Running at {source_path}')
    for f in os.listdir(source_path):
        if '.' in f:
            continue
        start_time = time.time()
        print(f'Running on article: {f}')

        result_file_path = f'{source_path}/{f}/tesseract-results.txt'
        if os.path.exists(result_file_path):
            print('Results exist')
            continue

        res = ''
        i = 0
        image_file_path = f'{source_path}/{f}/page-{i}.png'
        while (os.path.exists(image_file_path)):
            text = pytesseract.image_to_string(image_file_path, lang=language)
            res += ' '.join(text)
            i += 1
            image_file_path = f'{source_path}/{f}/page-{i}.png'
        with open(result_file_path, 'wt') as outfile:
            outfile.write(res)

        end_time = time.time()
        time_taken = end_time - start_time
        print(f'Finished! Time taken: {time_taken} seconds')


def run_tesseract(articles: List[str], source_path: str, language: str):
    """
    Runs Tesseract on selected articles in a directory and stores results in an output file.

    Args:
        articles: List of articles to perform EasyOCR on
        source_path: Path to articles
        language: Tesseract language code to detect. List of Tesseract language codes be found at: https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html.
    """
    for article in articles:
        start_time = time.time()
        print(f'Running on article: {article}')

        result_file_path = f'{source_path}/{article}/tesseract-results.txt'
        if os.path.exists(result_file_path):
            print('Results exist')
            continue

        res = ''
        i = 0
        image_file_path = f'{source_path}/{article}/page-{i}.png'
        while os.path.exists(image_file_path):
            text = pytesseract.image_to_string(image_file_path, lang=language)
            res += ' '.join(text)
            i += 1
            image_file_path = f'{source_path}/{article}/page-{i}.png'
        with open(result_file_path, 'wt') as outfile:
            outfile.write(res)

        end_time = time.time()
        time_taken = end_time - start_time
        print(f'Finished! Time taken: {time_taken} seconds')
