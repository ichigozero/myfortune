import requests

from bs4 import BeautifulSoup


class Scraper:
    def __init__(self):
        self._soup = None

    def get_soup(self, url):
        try:
            content = requests.get(url).content
            self._soup = BeautifulSoup(content, 'html.parser')
        except requests.exceptions.RequestException:
            pass
