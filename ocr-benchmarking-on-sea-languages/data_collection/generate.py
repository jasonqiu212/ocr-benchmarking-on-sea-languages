import os

from weasyprint import HTML


def generate_pdfs(source_path: str, font_path: str = None):
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
                }}
            </style>
        </head>
        '''
    else:
        html_head = ''

    for f in os.listdir(source_path):
        print(f'Running on article: {f}')

        text_file = f'{source_path}/{f}/text.txt'
        if not os.path.exists(text_file):
            print(f'{f}: text.txt does not exist')
            continue

        text = open(text_file, 'r').read()
        html_content = f'<html>{html_head}<body><p>{text}</p></body></html>'

        HTML(string=html_content, base_url='.').write_pdf(
            f'{source_path}/{f}/article.pdf')
