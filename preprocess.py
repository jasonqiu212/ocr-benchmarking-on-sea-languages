"""This file provides operations to preprocess article images."""

from os import listdir

import pymupdf


def convert_pdfs_to_pngs(source_path: str):
    """Converts and saves all PDFs into PNGs."""
    zoom_x = zoom_y = 2.0
    mat = pymupdf.Matrix(zoom_x, zoom_y)
    for f in listdir(source_path):
        path = f'{source_path}/{f}'
        pdf = pymupdf.open(f'{path}/article.pdf')
        for page in pdf:
            pix = page.get_pixmap(matrix=mat)
            pix.save(f'{path}/page-%i.png' % page.number)
