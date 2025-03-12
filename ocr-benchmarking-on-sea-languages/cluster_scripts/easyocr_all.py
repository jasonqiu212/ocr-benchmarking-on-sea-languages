import easyocr

import os
import time


def run_easy_ocr(easy_ocr_language: str, source_path: str):
    print(easy_ocr_language)
    reader = easyocr.Reader([easy_ocr_language])

    for f in os.listdir(source_path):
        start_time = time.time()

        result_file_path = f'{source_path}/{f}/easy-ocr-results.txt'
        if os.path.exists(result_file_path):
            print(f'{f}: Results exist')
            continue

        res = ''
        i = 0
        image_file_path = f'{source_path}/{f}/page-{i}.png'
        if not os.path.exists(image_file_path):
            print(f'{f}: Directory does not exist')
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
        print(f'{f}: {time_taken} seconds')


if __name__ == "__main__":
    easy_ocr_languages = [('english', 'en'),
                          ('indonesian', 'id'),
                          ('thai', 'th'),
                          ('vietnamese', 'vi')]
    noises = ['bold', 'italic', 'heading', 'link']

    for language_label, easy_ocr_language in easy_ocr_languages:
        for noise in noises:
            source_path = f'../../artificial_data_with_{noise}/{language_label}'
            run_easy_ocr(easy_ocr_language, source_path)
