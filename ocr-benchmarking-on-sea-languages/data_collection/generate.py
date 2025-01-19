import os

from PIL import Image, ImageDraw, ImageFont


def insert_character_at_nearest_space(text, char, n):
    result = []
    current_line = ""

    for word in text.split():
        # Check if adding the next word exceeds the limit
        if len(current_line) + len(word) + 1 > n:
            # Add the current line to the result and start a new line
            result.append(current_line.strip())
            current_line = word
        else:
            # Add the word to the current line
            current_line += " " + word

    # Append the remaining text
    if current_line:
        result.append(current_line.strip())

    # Join the lines with the specified character
    return char.join(result)


def insert_character_every_n_chars(text, char, n):
    # Insert `char` every `n` characters
    return char.join(text[i:i + n] for i in range(0, len(text), n))


img_width, img_height = 600, 12000
source = '../../data/vietnamese'

try:
    font = ImageFont.truetype("BeVietnamPro.ttf", size=20)
except:
    font = ImageFont.load_default()

for f in os.listdir(source):
    print(f'Running on article: {f}')

    text_file = f'{source}/{f}/text-clean.txt'
    if not os.path.exists(text_file):
        print(f'{f}: Clean does not exist')
        continue

    text = open(text_file, 'r').read(20000)

    artificial_text_file = f'{source}/{f}/text-artificial.txt'
    with open(artificial_text_file, 'w') as file:
        file.write(text)

    text = insert_character_at_nearest_space(text, '\n', 50)
    # text = insert_character_every_n_chars(text, '\n', 50)

    img = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.multiline_text((20, 20), text, fill=(0, 0, 0), font=font, spacing=5)

    img.save(f'{source}/{f}/artificial.png')
