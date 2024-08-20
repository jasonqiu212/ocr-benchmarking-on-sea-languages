"""
This class provides operations to download wikipedia articles in a PDF format.
Source: https://medium.com/@nikitatonkoshkur25/create-pdf-from-webpage-in-python-1e9603d6a430
"""

import base64
import json
import os
import time
from io import BytesIO
from typing import List

from selenium import webdriver


class WikipediaPdfGenerator:
    WIKIPEDIA_BASE_URLS = {
        'english': 'https://en.wikipedia.org/wiki',
        'thai': 'https://th.wikipedia.org/wiki',
        'vietnamese': 'https://vi.wikipedia.org/wiki',
    }

    driver = None
    print_options = {
        'landscape': False,
        'displayHeaderFooter': False,
        'printBackground': True,
        'preferCSSPageSize': True,
        'paperWidth': 6.97,
        'paperHeight': 16.5,
    }

    def __init__(self, language: str, path: str):
        if language not in self.WIKIPEDIA_BASE_URLS:
            raise Exception('Unrecognized language')

        self.base_url = self.WIKIPEDIA_BASE_URLS[language]
        self.destination_path = path

    def download_pdfs(self, titles: List[str]):
        pdf_files = self._generate_pdfs(titles)

        for title, pdf_file in pdf_files:
            file_path = f'{self.destination_path}/{title}'
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            with open(f'{file_path}/article.pdf', 'wb') as outfile:
                outfile.write(pdf_file.getbuffer())

    @staticmethod
    def _send_devtools(driver, cmd: str, params={}):
        """
        Works only with chromedriver.
        Method uses cromedriver's api to pass various commands to it.
        """
        resource = '/session/%s/chromium/send_command_and_get_result' % driver.session_id
        url = driver.command_executor._url + resource
        body = json.dumps({'cmd': cmd, 'params': params})
        response = driver.command_executor._request('POST', url, body)
        return response.get('value')

    def _generate_pdfs(self, titles: List[str]) -> List[BytesIO]:
        pdf_files = []
        try:
            self.driver = webdriver.Chrome()

            for title in titles:
                url = f'{self.base_url}/{title}'
                result = self._get_pdf_from_url(url)
                file = BytesIO()
                file.write(result)
                pdf_files.append((title, file))
        finally:
            self.driver.close()

        return pdf_files

    def _get_pdf_from_url(self, url: str):
        self.driver.get(url)

        time.sleep(0.3)  # allow the page to load, increase if needed

        print_options = self.print_options.copy()
        result = self._send_devtools(
            self.driver, 'Page.printToPDF', print_options)
        return base64.b64decode(result['data'])
