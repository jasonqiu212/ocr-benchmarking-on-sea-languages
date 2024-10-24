import os
import re

WIKIPEDIA_HEADERS = {
    'english': 'WIKIPEDIA The Free Encyclopedia',
    'thai': 'test',
    'bahasa': 'test',
    'vietnamese': 'test',
}

REFERENCES = {
    'english': 'References',
    'thai': 'test',
    'bahasa': 'test',
    'vietnamese': 'test',
}


def clean_easy_ocr(source_path: str, language: str):
    for article in os.listdir(source_path):
        dirty_file_path = f'{source_path}/{article}/easy-ocr-results.txt'
        if not os.path.exists(dirty_file_path):
            continue

        clean_file_path = f'{source_path}/{article}/easy-ocr-results-clean.txt'
        if os.path.exists(clean_file_path):
            continue

        dirty_text = open(dirty_file_path, 'r').read()

        res = re.sub(r'\[\d{1,4}\]', '', dirty_text)

        res = re.sub(WIKIPEDIA_HEADERS[language], '', res)

        try:
            index = res.rindex(REFERENCES[language])
            res = res[:index]
        except ValueError:
            pass

        res = res.strip()

        with open(clean_file_path, 'wt') as outfile:
            outfile.write(res)


def clean_tesseract(source_path: str, language: str):
    for article in os.listdir(source_path):
        dirty_file_path = f'{source_path}/{article}/tesseract-results.txt'
        if not os.path.exists(dirty_file_path):
            continue

        clean_file_path = f'{
            source_path}/{article}/tesseract-results-clean.txt'
        if os.path.exists(clean_file_path):
            continue

        dirty_lines = open(dirty_file_path, 'r').readlines()
        res = ''

        for dirty_line in dirty_lines:
            clean_line = dirty_line[1::2] if dirty_line[0] == ' ' else dirty_line[::2]
            res += clean_line

        res = re.sub(r'\[\d{1,4}\]', '', res)

        res = re.sub(WIKIPEDIA_HEADERS[language], '', res)

        try:
            index = res.rindex(REFERENCES[language])
            res = res[:index]
        except ValueError:
            pass

        res = res.strip()

    with open(clean_file_path, 'wt') as outfile:
        outfile.write(res)


def clean_ground_truth(source_path: str):
    pass
