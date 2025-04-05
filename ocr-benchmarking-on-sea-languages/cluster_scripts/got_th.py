from transformers import AutoModel, AutoTokenizer


tokenizer = AutoTokenizer.from_pretrained(
    'ucaslcl/GOT-OCR2_0', trust_remote_code=True)
model = AutoModel.from_pretrained('ucaslcl/GOT-OCR2_0', trust_remote_code=True, low_cpu_mem_usage=True,
                                  device_map='cuda', use_safetensors=True, pad_token_id=tokenizer.eos_token_id)
model = model.eval().cuda()

source_path = '../../artificial_data_for_finetuning_1200/thai/Apple'
test_image_name = 'page-0.png'

res = model.chat(tokenizer, f'{source_path}/{test_image_name}', ocr_type='ocr')
with open(f'{source_path}/got-results-page-0.txt', 'wt') as outfile:
    outfile.write(res)
