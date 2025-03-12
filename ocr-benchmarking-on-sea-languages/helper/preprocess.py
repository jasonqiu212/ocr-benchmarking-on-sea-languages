import os
from typing import List, Tuple

import pymupdf
from tqdm import tqdm


def convert_pdfs_to_pngs(source_path: str):
    """Converts and saves all PDFs into PNGs."""
    zoom_x = zoom_y = 2.0
    mat = pymupdf.Matrix(zoom_x, zoom_y)
    for f in tqdm(os.listdir(source_path)):
        path = f'{source_path}/{f}'
        pdf = pymupdf.open(f'{path}/article.pdf')
        for page in pdf:
            pix = page.get_pixmap(matrix=mat)
            pix.save(f'{path}/page-%i.png' % page.number)


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
