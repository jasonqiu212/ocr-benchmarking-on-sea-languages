import json
import os
import random


def prepare_dataset(source_path: str, output_file_name: str):
    dataset = []

    for article in os.listdir(source_path):
        i = 0
        while os.path.exists(f'{source_path}/{article}/page-{i}.png'):
            text_file_path = f'{source_path}/{article}/page-{i}-text.txt'
            text = open(text_file_path, 'r').read()

            image_path = f'{source_path}/{article}/page-{i}.png'
            data_entry = {
                'query': 'OCR <image>',
                'response': text,
                'images': [
                    image_path
                ]}
            dataset.append(data_entry)

            i += 1

    with open(f'{output_file_name}.json', 'w') as output_file:
        json.dump(dataset, output_file, ensure_ascii=False)


def train_test_split_from_dataset(source_path: str, dataset_file_name: str, num_of_test_samples: float):
    with open(f'{source_path}/{dataset_file_name}', 'r') as dataset_file:
        data = json.load(dataset_file)

        random.shuffle(data)
        test_dataset = data[:num_of_test_samples]
        train_dataset = data[num_of_test_samples:]

        with open(f'{source_path}/train.json', 'w') as train_dataset_file:
            json.dump(train_dataset, train_dataset_file, ensure_ascii=False)

        with open(f'{source_path}/test.json', 'w') as test_dataset_file:
            json.dump(test_dataset, test_dataset_file, ensure_ascii=False)


def select_samples_from_dataset(source_path: str, dataset_file_name: str, num_of_samples: str):
    with open(f'{source_path}/{dataset_file_name}', 'r') as dataset_file:
        data = json.load(dataset_file)

        random.shuffle(data)
        selected_dataset = data[:num_of_samples]

        with open(f'{source_path}/{num_of_samples}.json', 'w') as selected_dataset_file:
            json.dump(selected_dataset, selected_dataset_file,
                      ensure_ascii=False)
