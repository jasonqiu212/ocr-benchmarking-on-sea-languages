import json
import os


def prepare_dataset(source_path: str, output_file_name: str):
    dataset = []

    for article in os.listdir(source_path):
        i = 0
        while os.path.exists(f'{source_path}/{article}/page-{i}.png'):
            text_file_path = f'{source_path}/{article}/page-{i}-text.txt'
            text = open(text_file_path, 'r').read()

            image_path = f'{source_path}/{article}/page-{i}.png'
            data_entry = {
                'query': 'OCR',
                'response': text,
                'images': [
                    image_path
                ]}
            dataset.append(data_entry)

            i += 1

    with open(f'{output_file_name}.json', 'w') as output_file:
        json.dump(dataset, output_file, ensure_ascii=False)
