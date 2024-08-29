"""This file provides operations to download Wikipedia articles."""

import base64
import json
import os
import requests
import time
from io import BytesIO
from typing import List

from selenium import webdriver

from article_pdf import ArticlePDF

API_URLS = {
    'en': 'https://en.wikipedia.org/w/api.php',
    'th': 'https://th.wikipedia.org/w/api.php',
    'vi': 'https://vi.wikipedia.org/w/api.php',
    'id': 'https://id.wikipedia.org/w/api.php',
}


def download_article_texts(articles: List[ArticlePDF], destination_path: str):
    """
    Downloads and saves plain text from given articles into distinct folders named after the
    articles' respective English titles.

    Args:
        articles: List of articles to get plain text for
        destination_path: Destination path to save plain text files
    """
    query_parameters = {
        'action': 'query',
        'prop': 'extracts',
        'format': 'json',
        'explaintext': 'true',
    }
    for article in articles:
        title = article.title
        english_title = article.english_title
        language = article.language
        try:
            query_parameters['titles'] = title
            response = requests.get(API_URLS[language], query_parameters)
            data = response.json()
            text = list(data['query']['pages'].items())[0][1]['extract']

            file_path = f'{destination_path}/{english_title}'
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            with open(f'{file_path}/text.txt', 'wt') as outfile:
                outfile.write(text)
        except:
            print(f'Issue fetching for {english_title}')


def get_articles_by_language(articles: List[ArticlePDF], language: str) -> List[ArticlePDF]:
    """
    Fetches articles by language.

    Args:
        articles: List of articles in English
        language: Target language code to fetch

    Returns:
        List of articles in target language
    """
    query_parameters = {
        'action': 'query',
        'prop': 'langlinks',
        'llprop': 'url',
        'format': 'json'
    }
    query_parameters['lllang'] = language
    en_api_url = API_URLS['en']

    result_articles = []
    for article in articles:
        english_title = article.english_title

        query_parameters['titles'] = english_title
        try:
            response = requests.get(en_api_url, query_parameters)
            data = response.json()
            url = list(data['query']['pages'].items())[
                0][1]['langlinks'][0]['url']
            title = list(data['query']['pages'].items())[
                0][1]['langlinks'][0]['*']
            new_article = ArticlePDF(title, english_title, url, language)
            result_articles.append(new_article)
        except:
            print(f'Issue fetching for {english_title} in {language}')

    return result_articles


def download_article_pdfs(articles: List[ArticlePDF], destination_path: str):
    """
    Downloads and saves PDFs from given article URLs into distinct folders named after the
    articles' respective titles.

    Source: https://medium.com/@nikitatonkoshkur25/create-pdf-from-webpage-in-python-1e9603d6a430

    Args:
        articles: List of articles to get PDFs for
        destination_path: Destination path to save PDFs
    """
    article_pdfs = _generate_pdfs(articles)

    for article_pdf in article_pdfs:
        file_path = f'{destination_path}/{article_pdf.title}'
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        with open(f'{file_path}/article.pdf', 'wb') as outfile:
            outfile.write(article_pdf.file.getbuffer())


def _generate_pdfs(articles: List[ArticlePDF]) -> List[ArticlePDF]:
    """
    Generates and adds PDFs from given article URLs into given list of articles.

    Args:
        articles: List of articles to get PDFs for

    Returns:
        List of articles containing added PDFs
    """
    try:
        driver = webdriver.Chrome()
        for article in articles:
            result = _get_pdf(driver, article.url)
            file = BytesIO()
            file.write(result)
            article.file = file
    finally:
        driver.close()

    return articles


def _get_pdf(driver, url: str) -> bytes:
    """
    Gets PDF file of given URL.
    """
    driver.get(url)

    time.sleep(0.3)  # allow the page to load, increase if needed

    print_options = {
        'landscape': False,
        'displayHeaderFooter': False,
        'printBackground': True,
        'preferCSSPageSize': True,
        'paperWidth': 6.97,
        'paperHeight': 16.5,
    }
    result = _send_devtools(
        driver, 'Page.printToPDF', print_options)
    return base64.b64decode(result['data'])


def _send_devtools(driver, cmd: str, params={}):
    """
    Sends command to driver's dev tools.

    Works only with chromedriver, since method uses cromedriver's API to pass
    various commands to it.
    """
    resource = '/session/%s/chromium/send_command_and_get_result' % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    return response.get('value')
