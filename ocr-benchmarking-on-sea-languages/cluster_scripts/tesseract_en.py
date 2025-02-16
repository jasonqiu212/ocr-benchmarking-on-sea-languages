import os
import time

import pytesseract

source_path = '../../artificial_data/english'
language = 'eng'

for f in os.listdir(source_path):
    start_time = time.time()
    print(f'Running on article: {f}')

    result_file_path = f'{source_path}/{f}/tesseract-results.txt'
    if os.path.exists(result_file_path):
        print('Results exist')
        continue

    res = ''
    i = 0
    image_file_path = f'{source_path}/{f}/page-{i}.png'
    if not os.path.exists(image_file_path):
        print('Directory does not exist')
        continue

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
