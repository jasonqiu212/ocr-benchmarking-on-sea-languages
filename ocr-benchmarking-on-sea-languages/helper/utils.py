import os
from typing import List, Tuple


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


def count_article_pages(source_path: str):
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
