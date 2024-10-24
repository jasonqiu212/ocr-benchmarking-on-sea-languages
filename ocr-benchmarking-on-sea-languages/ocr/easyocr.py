import os
import time
from typing import List


def run_easy_ocr_on_all(source_path: str, reader):
    """
    Runs EasyOCR on all articles in a directory and stores results in an output file.

    Args:
        source_path: Path to articles
        reader: EasyOCR reader that specifies languages to recognize
    """
    print(f'Running at {source_path}')
    for f in os.listdir(source_path):
        start_time = time.time()
        print(f'Running on article: {f}')

        result_file_path = f'{source_path}/{f}/easy-ocr-results.txt'
        if os.path.exists(result_file_path):
            print('Results exist')
            continue

        res = ''
        i = 0
        image_file_path = f'{source_path}/{f}/page-{i}.png'
        if not os.path.exists(image_file_path):
            print('Directory does not exist')
            continue

        while os.path.exists(image_file_path):
            text = reader.readtext(image_file_path, detail=0)
            res += ' '.join(text)
            i += 1
            image_file_path = f'{source_path}/{f}/page-{i}.png'
        with open(result_file_path, 'wt') as outfile:
            outfile.write(res)

        end_time = time.time()
        time_taken = end_time - start_time
        print(f'Finished! Time taken: {time_taken} seconds')


def run_easy_ocr(articles: List[str], source_path: str, reader):
    """
    Runs EasyOCR on selected articles in a directory and stores results in an output file.

    Args:
        articles: List of articles to perform EasyOCR on
        source_path: Path to articles
        reader: EasyOCR reader that specifies languages to recognize
    """
    for article in articles:
        start_time = time.time()
        print(f'Running on article: {article}')

        result_file_path = f'{source_path}/{article}/easy-ocr-results.txt'
        if os.path.exists(result_file_path):
            print('Results exist')
            continue

        res = ''
        i = 0
        image_file_path = f'{source_path}/{article}/page-{i}.png'
        if not os.path.exists(image_file_path):
            print('Directory does not exist')
            continue
        while os.path.exists(image_file_path):
            text = reader.readtext(image_file_path, detail=0)
            res += ' '.join(text)
            i += 1
            image_file_path = f'{source_path}/{article}/page-{i}.png'
        with open(result_file_path, 'wt') as outfile:
            outfile.write(res)

        end_time = time.time()
        time_taken = end_time - start_time
        print(f'Finished! Time taken: {time_taken} seconds')
