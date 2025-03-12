import easyocr

import os
import time

vi_reader = easyocr.Reader(['vi'])
source_path = '../../artificial_data_with_bold/vietnamese'

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
        text = vi_reader.readtext(image_file_path, detail=0)
        res += ' '.join(text)
        i += 1
        image_file_path = f'{source_path}/{f}/page-{i}.png'
    with open(result_file_path, 'wt') as outfile:
        outfile.write(res)

    end_time = time.time()
    time_taken = end_time - start_time
    print(f'Finished! Time taken: {time_taken} seconds')
