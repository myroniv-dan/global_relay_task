import concurrent.futures
import logging
import os
from functools import partial

import pandas as pd
import requests
from bs4 import BeautifulSoup

from config import Paths
from utils import assure_path_exist

BASE_URL = 'https://www.voiptroubleshooter.com/open_speech/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}


class Crawler:

    def run(self):
        get_wav_metadata(get_pages())


def get_pages():

    page = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(page.content, features='html')

    uls = soup.find_all('ul')
    all_pages = []

    for li in uls[1].findAll('li'):
        if 'open_speech' in li.a.get('href'):
            all_pages.append(li.a.get('href').rsplit('/', 1)[1])
        else:
            all_pages.append(li.a.get('href'))

    logging.info(f'All Pages: {all_pages}')

    return all_pages


def get_wav_metadata(pages):

    for page in pages:

        lang = requests.get(BASE_URL + page, headers=HEADERS)
        dfs = pd.read_html(lang.text)

        df = dfs[1].iloc[1:, :]
        df = df.dropna()

        df = df.rename(
            columns={
                0: "file",
                1: "m/f",
                2: "format",
                3: "sample Rate",
                4: "description"
            })

        language = page[:-5]
        language = language.replace('india', 'hindi')

        assure_path_exist(Paths.METADATA)

        df.to_csv(os.path.join(Paths.METADATA, f'{language}.csv'))

        # logging.info(f'Language: {language} \n {df}')

        assure_path_exist(os.path.join(Paths.WAVS, language))

        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(partial(download_wav, language=language), df.file)


def download_wav(file, language):

    logging.info(f'Downloading: {file}')

    r = requests.get(BASE_URL + language + '/' + file, headers=HEADERS)
    with open(os.path.join(Paths.WAVS, language, file), 'wb') as f:
        f.write(r.content)
