"""This file provides operations to evaluate OCR performance."""

import csv
from collections import Counter
import json
import os
import re
import unicodedata

import jiwer
from Levenshtein import editops
from tqdm import tqdm


def evaluate(source_path: str, target_file_name: str, prediction_file_name: str, output_file_name: str):
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


def evaluate_finetuned(results_file_path: str, output_file_name: str):
    data = [['File Name', 'CER', 'WER']]
    with open(results_file_path, "r") as results_file:
        for line in results_file:
            results = json.loads(line)

            prediction_text = results['response']
            target_text = results['labels']
            file_name = '/'.join(results['images'][0]['path'].split('/')[-2:])

            cer = jiwer.cer(target_text, prediction_text)
            wer = jiwer.wer(target_text, prediction_text)

            formatted_cer = round(cer, 4)
            formatted_wer = round(wer, 4)
            data.append([file_name, formatted_cer, formatted_wer])

    with open(f'{output_file_name}.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(data)


def evaluate_error_by_character_class(source_path: str, correct_file_name: str, predicted_file_name: str, output_file_name: str):
    data = [['Article Name', 'arabic_digit', 'thai_digit', 'latin_letter', 'latin_letter_with_diacritic', 'thai_letter',
            'thai_diacritic', 'punctuation', 'thai_punctuation', 'vietnamese_punctuation', 'whitespace', 'other']]
    sorted_articles = sorted(os.listdir(source_path))

    for article in tqdm(sorted_articles):
        correct_file_path = f'{source_path}/{article}/{correct_file_name}'
        if not os.path.exists(correct_file_path):
            print(f'{article}: {correct_file_path} does not exist.')
            continue

        predicted_file_path = f'{source_path}/{article}/{predicted_file_name}'
        if not os.path.exists(predicted_file_path):
            print(f'{article}: {predicted_file_path} does not exist.')
            continue

        error_counts = Counter()

        correct = open(correct_file_path, 'r').read()
        predicted = open(predicted_file_path, 'r').read()
        operations = editops(correct, predicted)

        for operation, i, j in operations:
            if operation == 'replace':  # Substitution
                char_class = _classify_char(correct[i])
                error_counts[char_class] += 1
            elif operation == 'insert':  # Insertion in predicted
                char_class = _classify_char(predicted[j])
                error_counts[char_class] += 1
            elif operation == 'delete':  # Deletion from target
                char_class = _classify_char(correct[i])
                error_counts[char_class] += 1

        data.append([article, error_counts['arabic_digit'], error_counts['thai_digit'],
                     error_counts['latin_letter'], error_counts['latin_letter_with_diacritic'],
                     error_counts['thai_letter'], error_counts['thai_diacritic'], error_counts['punctuation'],
                    error_counts['thai_punctuation'], error_counts['vietnamese_punctuation'],
                    error_counts['whitespace'], error_counts['other']])

    with open(f'{source_path}/{output_file_name}.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(data)


def classify_by_character_class(source_path: str, input_file_name: str, output_file_name: str):
    data = [['Article Name', 'arabic_digit', 'thai_digit', 'latin_letter', 'latin_letter_with_diacritic', 'thai_letter',
            'thai_diacritic', 'punctuation', 'thai_punctuation', 'vietnamese_punctuation', 'whitespace', 'other']]
    sorted_articles = sorted(os.listdir(source_path))
    h = {}

    for article in tqdm(sorted_articles):
        input_file_path = f'{source_path}/{article}/{input_file_name}'
        if not os.path.exists(input_file_path):
            print(f'{article}: {input_file_path} does not exist.')
            continue

        counts = Counter()

        input = open(input_file_path, 'r').read()

        for c in input:
            char_class = _classify_char(c)
            if char_class == 'other':
                h[c] = h.get(c, 0) + 1
            counts[char_class] += 1

        data.append([article, counts['arabic_digit'], counts['thai_digit'],
                     counts['latin_letter'], counts['latin_letter_with_diacritic'],
                     counts['thai_letter'], counts['thai_diacritic'], counts['punctuation'],
                    counts['thai_punctuation'], counts['vietnamese_punctuation'],
                    counts['whitespace'], counts['other']])
    # print(dict(sorted(h.items(), key=lambda item: item[1], reverse=True)))

    with open(f'{source_path}/{output_file_name}.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(data)


def _classify_char(char: str):
    if char.isdigit():
        return "arabic_digit"
    if '๐' <= char <= '๙':
        return "thai_digit"

    elif 'A' <= char <= 'Z' or 'a' <= char <= 'z':
        return "latin_letter"
    elif re.match(r"[àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ]", char):
        return "latin_letter_with_diacritic"
    elif _is_thai_character(char):
        return "thai_letter"
    elif re.match(r"[่้๊๋็์]", char):
        return "thai_diacritic"

    elif re.match(r"[.,!?;:()\-\"']", char):
        return "punctuation"
    elif re.match(r"[ๆฯ]", char):
        return "thai_punctuation"
    elif re.match(r"[«»]", char):
        return "vietnamese_punctuation"

    elif char.isspace():  # Whitespace
        return "whitespace"

    else:
        return "other"


def _is_thai_character(char):
    try:
        name = unicodedata.name(char, '')
        return 'THAI CHARACTER' in name and not any(x in name for x in ['DIGIT', 'SIGN', 'MARK'])
    except ValueError:
        return False
