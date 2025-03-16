import time
import os
from transformers import AutoModel, AutoTokenizer

source_path = '../../artificial_data_v2/indonesian'

tokenizer = AutoTokenizer.from_pretrained(
    'ucaslcl/GOT-OCR2_0', trust_remote_code=True)
model = AutoModel.from_pretrained('ucaslcl/GOT-OCR2_0', trust_remote_code=True, low_cpu_mem_usage=True,
                                  device_map='cuda', use_safetensors=True, pad_token_id=tokenizer.eos_token_id)
model = model.eval().cuda()


for f in os.listdir(source_path):
    start_time = time.time()

    result_file_path = f'{source_path}/{f}/got-results.txt'
    if os.path.exists(result_file_path):
        print(f'{f}: Results exist')
        continue

    res = ''
    i = 0
    image_file_path = f'{source_path}/{f}/page-{i}.png'
    if not os.path.exists(image_file_path):
        print(f'{image_file_path}: Directory does not exist')
        continue

    while (os.path.exists(image_file_path)):
        text = model.chat(tokenizer, image_file_path, ocr_type='ocr')
        res += ' '.join(text)
        i += 1
        image_file_path = f'{source_path}/{f}/page-{i}.png'
    with open(result_file_path, 'wt') as outfile:
        outfile.write(res)

    end_time = time.time()
    time_taken = end_time - start_time
    print(f'{f}: {time_taken} seconds')
