from enum import Enum

import os
import random

import pymupdf
from tqdm import tqdm
from weasyprint import HTML


class Noise(Enum):
    BOLD = 1
    ITALIC = 2
    LINK = 3  # Blue and underline
    HEADING = 4


def generate_pdfs(source_path: str, font_path: str = None,
                  noise_type: Noise = None, noise_ratio: float = None):
    if font_path:
        html_head = f'''
        <head>
            <style>
                @font-face {{
                    font-family: 'CustomFont';
                    src: url('{font_path}') format('truetype');
                }}
                body {{
                    font-family: 'CustomFont', sans-serif;
                    line-height: 1.5;
                }}
            </style>
        </head>
        '''
    else:
        html_head = ''

    for f in tqdm(os.listdir(source_path)):
        text_file = f'{source_path}/{f}/text.txt'
        if not os.path.exists(text_file):
            print(f'{f}: text.txt does not exist')
            continue

        text = open(text_file, 'r').read()

        if noise_type and noise_ratio:
            # TODO: abstract out components into methods
            match noise_type:
                case Noise.BOLD:
                    words = text.split()
                    num_bold = int(len(words) * noise_ratio)
                    bold_indices = set(random.sample(
                        range(len(words)), num_bold))
                    result = [
                        f'<b>{word}</b>' if i in bold_indices else word
                        for i, word in enumerate(words)
                    ]
                    text = ' '.join(result)
                case Noise.ITALIC:
                    words = text.split()
                    num_bold = int(len(words) * noise_ratio)
                    bold_indices = set(random.sample(
                        range(len(words)), num_bold))
                    result = [
                        f'<i>{word}</i>' if i in bold_indices else word
                        for i, word in enumerate(words)
                    ]
                    text = ' '.join(result)
                case Noise.LINK:
                    words = text.split()
                    num_bold = int(len(words) * noise_ratio)
                    bold_indices = set(random.sample(
                        range(len(words)), num_bold))
                    result = [
                        f'<a href="#">{word}</a>' if i in bold_indices else word
                        for i, word in enumerate(words)
                    ]
                    text = ' '.join(result)
                case Noise.HEADING:
                    words = text.split()
                    num_bold = int(len(words) * noise_ratio)
                    bold_indices = set(random.sample(
                        range(len(words)), num_bold))
                    result = [
                        f'<h1>{word}</h1>' if i in bold_indices else word
                        for i, word in enumerate(words)
                    ]
                    text = ' '.join(result)
                case _:
                    pass

            with open(f'{source_path}/{f}/html-body.txt', 'w') as file:
                file.write(text)

        html_content = f'<html>{html_head}<body><p style="line-height: 2;">{text}</p></body></html>'

        HTML(string=html_content, base_url='.').write_pdf(
            f'{source_path}/{f}/article.pdf')


def get_page_text(source_path: str):
    for f in tqdm(os.listdir(source_path)):
        pdf_file = f'{source_path}/{f}/article.pdf'
        if not os.path.exists(pdf_file):
            print(f'{f}: article.pdf does not exist')
            continue

        pdf_document = pymupdf.open(pdf_file)

        for i, page in enumerate(pdf_document):
            text = " ".join(page.get_text('text').splitlines())
            with open(f'{source_path}/{f}/page-{i}-text.txt', 'w') as output_file:
                output_file.write(text)
