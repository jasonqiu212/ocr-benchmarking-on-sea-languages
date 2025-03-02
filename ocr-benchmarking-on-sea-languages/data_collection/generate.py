import os

# from PIL import Image, ImageDraw, ImageFont
from weasyprint import HTML


def generate_pdfs(source_path):
    for f in os.listdir(source_path):
        print(f'Running on article: {f}')

        text_file = f'{source_path}/{f}/text.txt'
        if not os.path.exists(text_file):
            print(f'{f}: text.txt does not exist')
            continue

        text = open(text_file, 'r').read()
        html_content = f"<html><body><p>{text}</p></body></html>"

        HTML(string=html_content).write_pdf(f'{source_path}/{f}/article.pdf')


# def insert_character_at_nearest_space(text, char, n):
#     result = []
#     current_line = ""

#     for word in text.split():
#         # Check if adding the next word exceeds the limit
#         if len(current_line) + len(word) + 1 > n:
#             # Add the current line to the result and start a new line
#             result.append(current_line.strip())
#             current_line = word
#         else:
#             # Add the word to the current line
#             current_line += " " + word

#     # Append the remaining text
#     if current_line:
#         result.append(current_line.strip())

#     # Join the lines with the specified character
#     return char.join(result)


# def insert_character_every_n_chars(text, char, n):
#     return char.join(text[i:i + n] for i in range(0, len(text), n))


# img_width, img_height = 600, 1000
# source_path = '../../data/thai'
# destination_path = '../../artificial_data/thai'

# try:
#     font = ImageFont.truetype("NotoSansThai.ttf", size=20)
# except:
#     font = ImageFont.load_default()

# for f in os.listdir(source_path):
#     print(f'Running on article: {f}')

#     text_file = f'{destination_path}/{f}/text.txt'
#     if not os.path.exists(text_file):
#         print(f'{f}: Text does not exist')
#         continue

#     text = open(text_file, 'r').read()

#     # artificial_text_file = f'{source}/{f}/text-artificial.txt'
#     # with open(artificial_text_file, 'w') as file:
#     #     file.write(text)

#     # text = insert_character_at_nearest_space(text, '\n', 50)
#     text = insert_character_every_n_chars(text, '\n', 50)

#     lines = text.split('\n')

#     lines = [s for s in lines if s]

#     lines_per_page = 34
#     line_count = 0
#     page_count = 0
#     while line_count < len(lines):
#         lines_to_draw = '\n'.join(
#             lines[line_count:line_count + lines_per_page])
#         img = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))
#         draw = ImageDraw.Draw(img)

#         draw.multiline_text((20, 20), lines_to_draw, fill=(
#             0, 0, 0), font=font, spacing=5)
#         img.save(f'{destination_path}/{f}/page-{page_count}.png')

#         line_count += lines_per_page
#         page_count += 1
