import os

import pandas as pd

from tqdm import tqdm
from sklearn.model_selection import train_test_split

source_path = '../../artificial_data_v2/thai'

df = pd.DataFrame(columns=['image_file_path', 'text_file'])

for f in tqdm(os.listdir(source_path)):
    i = 0
    while True:
        image_file_path = f'{f}/page-{i}.png'
        text_file_path = f'{f}/page-{i}-text.txt'

        if not os.path.exists(f'{source_path}/{image_file_path}') or not os.path.exists(f'{source_path}/{text_file_path}'):
            break

        df.loc[len(df)] = [image_file_path, text_file_path]
        i += 1

print(df.head())
