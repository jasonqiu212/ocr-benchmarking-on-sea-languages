import time
import os
from transformers import AutoModel, AutoTokenizer

source_path = '../../artificial_data_v2/vietnamese'

tokenizer = AutoTokenizer.from_pretrained(
    'ucaslcl/GOT-OCR2_0', trust_remote_code=True)
model = AutoModel.from_pretrained('ucaslcl/GOT-OCR2_0', trust_remote_code=True, low_cpu_mem_usage=True,
                                  device_map='cuda', use_safetensors=True, pad_token_id=tokenizer.eos_token_id)
model = model.eval().cuda()

test_image_paths = ['../../artificial_data_for_finetuning_1200/vietnamese/Spain/page-7.png', '../../artificial_data_for_finetuning_1200/vietnamese/Taylor_Swift/page-0.png', '../../artificial_data_for_finetuning_1200/vietnamese/Sun/page-13.png', '../../artificial_data_for_finetuning_1200/vietnamese/Cat/page-7.png', '../../artificial_data_for_finetuning_1200/vietnamese/Tiger/page-4.png', '../../artificial_data_for_finetuning_1200/vietnamese/Elephant/page-4.png', '../../artificial_data_for_finetuning_1200/vietnamese/Michael_Jackson/page-3.png', '../../artificial_data_for_finetuning_1200/vietnamese/Great_Wall_of_China/page-4.png', '../../artificial_data_for_finetuning_1200/vietnamese/Singapore/page-9.png', '../../artificial_data_for_finetuning_1200/vietnamese/Rome/page-9.png', '../../artificial_data_for_finetuning_1200/vietnamese/Stonehenge/page-0.png', '../../artificial_data_for_finetuning_1200/vietnamese/Stephen_Hawking/page-2.png', '../../artificial_data_for_finetuning_1200/vietnamese/Bird/page-5.png', '../../artificial_data_for_finetuning_1200/vietnamese/Freddie_Mercury/page-5.png', '../../artificial_data_for_finetuning_1200/vietnamese/Snake/page-2.png', '../../artificial_data_for_finetuning_1200/vietnamese/Brazil/page-7.png', '../../artificial_data_for_finetuning_1200/vietnamese/Barack_Obama/page-8.png', '../../artificial_data_for_finetuning_1200/vietnamese/Taj_Mahal/page-0.png', '../../artificial_data_for_finetuning_1200/vietnamese/Chicago/page-4.png', '../../artificial_data_for_finetuning_1200/vietnamese/Philippines/page-0.png', '../../artificial_data_for_finetuning_1200/vietnamese/London/page-8.png', '../../artificial_data_for_finetuning_1200/vietnamese/London/page-3.png', '../../artificial_data_for_finetuning_1200/vietnamese/Moon/page-13.png', '../../artificial_data_for_finetuning_1200/vietnamese/Mumbai/page-7.png', '../../artificial_data_for_finetuning_1200/vietnamese/Pluto/page-1.png',
                    '../../artificial_data_for_finetuning_1200/vietnamese/Big_Bang/page-21.png', '../../artificial_data_for_finetuning_1200/vietnamese/Moon/page-14.png', '../../artificial_data_for_finetuning_1200/vietnamese/Eiffel_Tower/page-0.png', '../../artificial_data_for_finetuning_1200/vietnamese/Ukraine/page-9.png', '../../artificial_data_for_finetuning_1200/vietnamese/Moon/page-25.png', '../../artificial_data_for_finetuning_1200/vietnamese/Lion/page-5.png', '../../artificial_data_for_finetuning_1200/vietnamese/Golden_Gate_Bridge/page-0.png', '../../artificial_data_for_finetuning_1200/vietnamese/Galaxy/page-18.png', '../../artificial_data_for_finetuning_1200/vietnamese/Bird/page-0.png', '../../artificial_data_for_finetuning_1200/vietnamese/Moon/page-6.png', '../../artificial_data_for_finetuning_1200/vietnamese/Washington,_D.C./page-0.png', '../../artificial_data_for_finetuning_1200/vietnamese/Andromeda_Galaxy/page-1.png', '../../artificial_data_for_finetuning_1200/vietnamese/Elephant/page-7.png', '../../artificial_data_for_finetuning_1200/vietnamese/Big_Bang/page-22.png', '../../artificial_data_for_finetuning_1200/vietnamese/Israel/page-8.png', '../../artificial_data_for_finetuning_1200/vietnamese/Boston/page-4.png', '../../artificial_data_for_finetuning_1200/vietnamese/Hong_Kong/page-8.png', '../../artificial_data_for_finetuning_1200/vietnamese/Mammal/page-2.png', '../../artificial_data_for_finetuning_1200/vietnamese/Jupiter/page-7.png', '../../artificial_data_for_finetuning_1200/vietnamese/Potato/page-6.png', '../../artificial_data_for_finetuning_1200/vietnamese/Boston/page-1.png', '../../artificial_data_for_finetuning_1200/vietnamese/Uranus/page-21.png', '../../artificial_data_for_finetuning_1200/vietnamese/Freddie_Mercury/page-3.png', '../../artificial_data_for_finetuning_1200/vietnamese/Venus/page-6.png', '../../artificial_data_for_finetuning_1200/vietnamese/Chicago/page-1.png']

for image_path in test_image_paths:
    start_time = time.time()

    page_number = int(image_path.split('/')[-1][5:-4])
    folder_path = '/'.join(image_path.split('/')[:-1])

    result_file_path = f'{folder_path}/got-results-page-{page_number}.txt'
    if os.path.exists(result_file_path):
        print(f'{image_path}: Results exist')
        continue

    if not os.path.exists(image_path):
        print(f'{image_path}: Directory does not exist')
        continue

    res = model.chat(tokenizer, image_path, ocr_type='ocr')
    with open(result_file_path, 'wt') as outfile:
        outfile.write(res)

    end_time = time.time()
    time_taken = end_time - start_time
    print(f'{image_path}: {time_taken} seconds')
