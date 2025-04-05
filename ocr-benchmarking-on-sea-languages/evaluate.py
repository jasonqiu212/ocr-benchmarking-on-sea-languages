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

a = [('../artificial_data_for_finetuning_1200/vietnamese/Spain/got-results-page-7.txt', '../artificial_data_for_finetuning_1200/vietnamese/Spain/page-7-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Taylor_Swift/got-results-page-0.txt', '../artificial_data_for_finetuning_1200/vietnamese/Taylor_Swift/page-0-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Sun/got-results-page-13.txt', '../artificial_data_for_finetuning_1200/vietnamese/Sun/page-13-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Cat/got-results-page-7.txt', '../artificial_data_for_finetuning_1200/vietnamese/Cat/page-7-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Tiger/got-results-page-4.txt', '../artificial_data_for_finetuning_1200/vietnamese/Tiger/page-4-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Elephant/got-results-page-4.txt', '../artificial_data_for_finetuning_1200/vietnamese/Elephant/page-4-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Michael_Jackson/got-results-page-3.txt', '../artificial_data_for_finetuning_1200/vietnamese/Michael_Jackson/page-3-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Great_Wall_of_China/got-results-page-4.txt', '../artificial_data_for_finetuning_1200/vietnamese/Great_Wall_of_China/page-4-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Singapore/got-results-page-9.txt', '../artificial_data_for_finetuning_1200/vietnamese/Singapore/page-9-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Rome/got-results-page-9.txt', '../artificial_data_for_finetuning_1200/vietnamese/Rome/page-9-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Stonehenge/got-results-page-0.txt', '../artificial_data_for_finetuning_1200/vietnamese/Stonehenge/page-0-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Stephen_Hawking/got-results-page-2.txt', '../artificial_data_for_finetuning_1200/vietnamese/Stephen_Hawking/page-2-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Bird/got-results-page-5.txt', '../artificial_data_for_finetuning_1200/vietnamese/Bird/page-5-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Freddie_Mercury/got-results-page-5.txt', '../artificial_data_for_finetuning_1200/vietnamese/Freddie_Mercury/page-5-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Snake/got-results-page-2.txt', '../artificial_data_for_finetuning_1200/vietnamese/Snake/page-2-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Brazil/got-results-page-7.txt', '../artificial_data_for_finetuning_1200/vietnamese/Brazil/page-7-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Barack_Obama/got-results-page-8.txt', '../artificial_data_for_finetuning_1200/vietnamese/Barack_Obama/page-8-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Taj_Mahal/got-results-page-0.txt', '../artificial_data_for_finetuning_1200/vietnamese/Taj_Mahal/page-0-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Chicago/got-results-page-4.txt', '../artificial_data_for_finetuning_1200/vietnamese/Chicago/page-4-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Philippines/got-results-page-0.txt', '../artificial_data_for_finetuning_1200/vietnamese/Philippines/page-0-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/London/got-results-page-8.txt', '../artificial_data_for_finetuning_1200/vietnamese/London/page-8-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/London/got-results-page-3.txt', '../artificial_data_for_finetuning_1200/vietnamese/London/page-3-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Moon/got-results-page-13.txt', '../artificial_data_for_finetuning_1200/vietnamese/Moon/page-13-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Mumbai/got-results-page-7.txt', '../artificial_data_for_finetuning_1200/vietnamese/Mumbai/page-7-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Pluto/got-results-page-1.txt', '../artificial_data_for_finetuning_1200/vietnamese/Pluto/page-1-text.txt'),
     ('../artificial_data_for_finetuning_1200/vietnamese/Big_Bang/got-results-page-21.txt', '../artificial_data_for_finetuning_1200/vietnamese/Big_Bang/page-21-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Moon/got-results-page-14.txt', '../artificial_data_for_finetuning_1200/vietnamese/Moon/page-14-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Eiffel_Tower/got-results-page-0.txt', '../artificial_data_for_finetuning_1200/vietnamese/Eiffel_Tower/page-0-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Ukraine/got-results-page-9.txt', '../artificial_data_for_finetuning_1200/vietnamese/Ukraine/page-9-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Moon/got-results-page-25.txt', '../artificial_data_for_finetuning_1200/vietnamese/Moon/page-25-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Lion/got-results-page-5.txt', '../artificial_data_for_finetuning_1200/vietnamese/Lion/page-5-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Golden_Gate_Bridge/got-results-page-0.txt', '../artificial_data_for_finetuning_1200/vietnamese/Golden_Gate_Bridge/page-0-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Galaxy/got-results-page-18.txt', '../artificial_data_for_finetuning_1200/vietnamese/Galaxy/page-18-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Bird/got-results-page-0.txt', '../artificial_data_for_finetuning_1200/vietnamese/Bird/page-0-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Moon/got-results-page-6.txt', '../artificial_data_for_finetuning_1200/vietnamese/Moon/page-6-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Washington,_D.C./got-results-page-0.txt', '../artificial_data_for_finetuning_1200/vietnamese/Washington,_D.C./page-0-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Andromeda_Galaxy/got-results-page-1.txt', '../artificial_data_for_finetuning_1200/vietnamese/Andromeda_Galaxy/page-1-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Elephant/got-results-page-7.txt', '../artificial_data_for_finetuning_1200/vietnamese/Elephant/page-7-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Big_Bang/got-results-page-22.txt', '../artificial_data_for_finetuning_1200/vietnamese/Big_Bang/page-22-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Israel/got-results-page-8.txt', '../artificial_data_for_finetuning_1200/vietnamese/Israel/page-8-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Boston/got-results-page-4.txt', '../artificial_data_for_finetuning_1200/vietnamese/Boston/page-4-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Hong_Kong/got-results-page-8.txt', '../artificial_data_for_finetuning_1200/vietnamese/Hong_Kong/page-8-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Mammal/got-results-page-2.txt', '../artificial_data_for_finetuning_1200/vietnamese/Mammal/page-2-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Jupiter/got-results-page-7.txt', '../artificial_data_for_finetuning_1200/vietnamese/Jupiter/page-7-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Potato/got-results-page-6.txt', '../artificial_data_for_finetuning_1200/vietnamese/Potato/page-6-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Boston/got-results-page-1.txt', '../artificial_data_for_finetuning_1200/vietnamese/Boston/page-1-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Uranus/got-results-page-21.txt', '../artificial_data_for_finetuning_1200/vietnamese/Uranus/page-21-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Freddie_Mercury/got-results-page-3.txt', '../artificial_data_for_finetuning_1200/vietnamese/Freddie_Mercury/page-3-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Venus/got-results-page-6.txt', '../artificial_data_for_finetuning_1200/vietnamese/Venus/page-6-text.txt'), ('../artificial_data_for_finetuning_1200/vietnamese/Chicago/got-results-page-1.txt', '../artificial_data_for_finetuning_1200/vietnamese/Chicago/page-1-text.txt')]

data = [['Article Name', 'CER', 'WER']]

for p, t in tqdm(a):
    article = p.split('/')[-2]
    if os.path.exists(p) and os.path.exists(t):
        target_text = open(t, 'r').read()
        prediction_text = open(p, 'r').read()

        cer = jiwer.cer(target_text, prediction_text)
        wer = jiwer.wer(target_text, prediction_text)

        formatted_cer = round(cer, 4)
        formatted_wer = round(wer, 4)
        data.append([article, formatted_cer, formatted_wer])

with open(f'./e.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)


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
    data = [['Article Name', 'arabic_digit', 'latin_letter', 'latin_letter_with_diacritic', 'vietnamese_special_letter', 'thai_letter',
             'special_symbol', 'whitespace', 'other']]
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

        data.append([article, error_counts['arabic_digit'],
                     error_counts['latin_letter'], error_counts['latin_letter_with_diacritic'],
                     error_counts['vietnamese_special_letter'],
                     error_counts['thai_letter'], error_counts['special_symbol'],
                    error_counts['whitespace'], error_counts['other']])

    with open(f'{source_path}/{output_file_name}.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(data)


def classify_by_character_class(source_path: str, input_file_name: str, output_file_name: str):
    data = [['Article Name', 'arabic_digit', 'latin_letter', 'latin_letter_with_diacritic', 'vietnamese_special_letter', 'thai_letter',
            'special_symbol', 'whitespace', 'other']]
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

        data.append([article, counts['arabic_digit'],
                     counts['latin_letter'], counts['latin_letter_with_diacritic'], counts['vietnamese_special_letter'],
                     counts['thai_letter'], counts['special_symbol'],
                    counts['whitespace'], counts['other']])
    # print(dict(sorted(h.items(), key=lambda item: item[1], reverse=True)))

    with open(f'{source_path}/{output_file_name}.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(data)


def _classify_char(char: str):
    if char.isdigit():
        return "arabic_digit"

    elif 'A' <= char <= 'Z' or 'a' <= char <= 'z':
        return "latin_letter"
    elif re.match(r"[àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ]", char.lower()):
        return "latin_letter_with_diacritic"
    elif char in ['đ', 'Đ']:
        return "vietnamese_special_letter"
    elif _is_thai_character(char):
        return "thai_letter"

    elif re.match(r"[.,!?;:()\-\–\—\"'$%/&+-=\[\]]", char):
        return "special_symbol"

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
