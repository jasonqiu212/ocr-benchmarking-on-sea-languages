"""This class encapsulates a Wikipedia article in any language."""


class ArticlePDF:
    file = None

    def __init__(self, title: str, english_title: str, url: str, language: str):
        self.title = title
        self.english_title = english_title
        self.url = url
        self.language = language
