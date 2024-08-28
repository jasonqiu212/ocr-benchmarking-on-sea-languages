from io import BytesIO


class ArticlePDF:
    def __init__(self, title: str, url: str, file: BytesIO = None):
        self.title = title
        self.url = url
        self.file = file
