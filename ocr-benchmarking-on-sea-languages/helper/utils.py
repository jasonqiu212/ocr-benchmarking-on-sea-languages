import csv
import os
from typing import List, Tuple

import pymupdf


def get_articles_sorted_by_length(source_path: str) -> List[Tuple[str, int]]:
    """
    Get articles sorted by length.

    Args:
        source_path: Path to get all articles

    Returns:
        List of articles in source path ranked in increasing lengths
    """
    res = []

    for f in os.listdir(source_path):
        i = 0
        image_file_path = f'{source_path}/{f}/page-{i}.png'
        while os.path.exists(image_file_path):
            i += 1
            image_file_path = f'{source_path}/{f}/page-{i}.png'
        res.append((f, i))

    return sorted(res, key=lambda x: x[1])


def count_article_pages_from_images(source_path: str):
    res = []
    for article in os.listdir(source_path):
        i = 0
        image_file_path = f'{source_path}/{article}/page-{i}.png'
        if not os.path.exists(image_file_path):
            continue

        while os.path.exists(image_file_path):
            i += 1
            image_file_path = f'{source_path}/{article}/page-{i}.png'

        res.append((article, i))
    return sorted(res)


def count_article_pages_from_pdf(source_path: str):
    res = []
    for article in os.listdir(source_path):
        pdf_file_path = f'{source_path}/{article}/article.pdf'
        if not os.path.exists(pdf_file_path):
            print(f'{article}: article.pdf does not exist')
            continue

        article_pdf = pymupdf.open(pdf_file_path)
        res.append((article, article_pdf.page_count))
        article_pdf.close()

    return sorted(res)


def write_to_csv(data: List, output_file_name: str):
    with open(f'./{output_file_name}.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data)
