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
                'query': 'OCR <image>',
                'response': text,
                'images': [
                    image_path
                ]}
            dataset.append(data_entry)

            i += 1

    with open(f'{output_file_name}.json', 'w') as output_file:
        json.dump(dataset, output_file, ensure_ascii=False)


def prepare_dataset_v2(source_path: str, output_file_name: str):
    problems = ['Adolf_Hitler/page-2.png', 'Adolf_Hitler/page-7.png', 'Canada/page-7.png', 'Eminem/page-5.png', 'Game_of_Thrones/page-1.png', 'Japan/page-1.png', 'Jerusalem/page-4.png', 'Johnny_Depp/page-7.png', 'Justin_Bieber/page-5.png',
                'Lionel_Messi/page-8.png', 'Machu_Picchu/page-3.png', 'Michael_Jackson/page-1.png', 'Spain/page-6.png', 'Steve_Jobs/page-8.png', 'United_Kingdom/page-0.png', 'United_States/page-6.png', 'Washington,_D.C./page-8.png']
    dataset = []

    for problem in problems:
        problem_no_ext = problem.replace('.png', '')
        number = int(problem_no_ext.split('-')[-1])
        article = problem_no_ext.split('/')[0]

        text_file_path = f'{source_path}/{article}/page-{number}-text.txt'
        text = open(text_file_path, 'r').read()

        image_path = f'{source_path}/{article}/page-{number}.png'
        data_entry = {
            'query': 'OCR <image>',
            'response': text,
            'images': [
                image_path
            ]}
        dataset.append(data_entry)

    with open(f'{output_file_name}.json', 'w') as output_file:
        json.dump(dataset, output_file, ensure_ascii=False)
