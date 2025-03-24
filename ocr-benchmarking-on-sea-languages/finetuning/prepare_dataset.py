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

# Good in vi-1200, but bad in vi-500
# Japan/page-1.png
# Michael_Jackson/page-1.png

# Good in vi-500, but bad in vi-1200
# India/page-7.png

# no pages that are bad for both vi-500 and vi-1200


def prepare_dataset_v2(source_path: str, output_file_name: str):
    problems = ['Adolf_Hitler/page-2.png', 'Canada/page-7.png', 'Eminem/page-5.png', 'Japan/page-1.png',
                'Lionel_Messi/page-8.png', 'Machu_Picchu/page-3.png', 'Spain/page-6.png', 'Steve_Jobs/page-8.png', 'United_Kingdom/page-7.png', 'Washington,_D.C./page-8.png']
    # problems = ['Andromeda_Galaxy/page-2.png', 'Australia/page-4.png', 'Big_Bang/page-1.png', 'Big_Bang/page-11.png', 'Big_Bang/page-15.png', 'Big_Bang/page-18.png', 'Big_Bang/page-20.png', 'Cat/page-3.png', 'Donald_Trump/page-0.png', 'Donald_Trump/page-4.png', 'Eiffel_Tower/page-6.png', 'Elon_Musk/page-9.png', 'Germany/page-4.png', 'Germany/page-7.png', 'Golden_Gate_Bridge/page-1.png', 'India/page-7.png', 'India/page-9.png', 'Israel/page-8.png', 'Jerusalem/page-3.png', 'Jupiter/page-12.png', 'Jupiter/page-5.png', 'Justin_Bieber/page-0.png',
    #             'Machu_Picchu/page-0.png', 'Moon/page-1.png', 'Moon/page-7.png', 'Neptune/page-3.png', 'Neptune/page-6.png', 'New Zealand/page-6.png', 'Pakistan/page-0.png', 'Pakistan/page-1.png', 'Panama_Canal/page-6.png', 'Philippines/page-4.png', 'Pluto/page-19.png', 'Potato/page-6.png', 'San_Francisco/page-2.png', 'San_Francisco/page-5.png', 'Spain/page-5.png', 'Stephen_Hawking/page-8.png', 'Sun/page-11.png', 'Sun/page-22.png', 'Sun/page-4.png', 'Sun/page-6.png', 'Toronto/page-2.png', 'United_Kingdom/page-8.png', 'Universe/page-15.png', 'Venus/page-22.png']
    # problems = ['Italy/page-7.png', 'Galaxy/page-4.png',
    #             'Cambodia/page-7.png', 'Big_Bang/page-9.png', 'Bangkok/page-7.png']

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
