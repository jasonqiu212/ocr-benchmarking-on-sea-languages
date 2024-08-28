"""This file provides operations to download Wikipedia articles."""

import base64
import json
import os
import requests
import time
from io import BytesIO
from typing import List

import wikipedia
from selenium import webdriver

from article_pdf import ArticlePDF


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


def get_articles_by_language(articles: List[ArticlePDF], language: str) -> List[ArticlePDF]:
    """
    Fetches articles' titles and URLs by language.

    Args:
        articles: List of articles with titles and URLs in English
        language: Target language to fetch

    Returns:
        List of articles with titles in English and URLs in target language
    """
    API_URL = 'https://en.wikipedia.org/w/api.php'
    query_parameters = {
        'action': 'query',
        'prop': 'langlinks',
        'llprop': 'url',
        'format': 'json'
    }
    query_parameters['lllang'] = language

    result_articles = []
    for article in articles:
        title = article.title

        query_parameters['titles'] = title
        try:
            response = requests.get(API_URL, query_parameters)
            data = response.json()
            url = list(data['query']['pages'].items())[
                0][1]['langlinks'][0]['url']
            result_articles.append(ArticlePDF(title, url))
        except:
            print(f'Issue fetching for {title} in {language}')

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
