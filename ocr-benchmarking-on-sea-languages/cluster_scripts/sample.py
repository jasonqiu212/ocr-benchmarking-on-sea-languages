import easyocr

from ocr.easyocr import run_easy_ocr_on_all

# This needs to run only once to load the model into memory
en_reader = easyocr.Reader(['en'])
th_reader = easyocr.Reader(['th'])
vi_reader = easyocr.Reader(['vi'])
id_reader = easyocr.Reader(['id'])


run_easy_ocr_on_all('../data/english', en_reader)
run_easy_ocr_on_all('../data/thai', th_reader)
run_easy_ocr_on_all('../data/vietnamese', vi_reader)
run_easy_ocr_on_all('../data/bahasa', id_reader)
