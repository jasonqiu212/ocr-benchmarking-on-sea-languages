"""This file provides operations to download Wikipedia articles."""

import os
from typing import List

import wikipedia


def download_article_texts(titles: List[str], destination_path: str):
    titles_with_space = list(
        map(lambda title: title.replace('_', ' '), titles))

    for title, title_with_space in zip(titles, titles_with_space):
        file_path = f'{destination_path}/{title}'
        article_text = get_article_text(title_with_space)

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        with open(f'{file_path}/text.txt', 'wt') as outfile:
            outfile.write(article_text)


def get_article_text(title: str) -> str:
    return wikipedia.WikipediaPage(title).content
