import re
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


TV_ASAHI_URL = 'https://www.tv-asahi.co.jp/goodmorning/uranai/'


class TvAsahiScraper(Scraper):
    def get_soup(self):
        super().get_soup(TV_ASAHI_URL)

    def extract_all_horoscope_readings(self):
        readings = {}

        try:
            rank_box = self._soup.find('ul', class_='rank-box')
            li_tags = rank_box.find_all('li')

            for rank_index, li_tag in enumerate(li_tags, start=1):
                zodiac_sign = li_tag.find('span').get_text(strip=True)
                readings[zodiac_sign] = {'rank': rank_index}

            seiza_boxes = self._soup.find_all('div', class_='seiza-box')

            for seiza_box in seiza_boxes:
                seiza_text = (
                    seiza_box.
                    find('p', class_='seiza-txt')
                    .get_text(strip=True)
                )
                zodiac_sign = re.search(r'(.*)\(.*\)', seiza_text).group(1)
                forecast = (
                    seiza_box
                    .find('p', class_='read')
                    .get_text(strip=True)
                )
                key_of_fortune = (
                    seiza_box
                    .find('div', class_='read-area')
                    .contents[8]
                    .replace('：', '')
                    .strip()
                )
                lucky_color = (
                    seiza_box
                    .find('div', class_='read-area')
                    .contents[4]
                    .replace('：', '')
                    .strip()
                )
                lucky_money = len(
                    seiza_box
                    .find('li', class_='lucky-money')
                    .find_all('img', class_='icon-money')
                )
                lucky_love = len(
                    seiza_box
                    .find('li', class_='lucky-love')
                    .find_all('img', class_='icon-love')
                )
                lucky_work = len(
                    seiza_box
                    .find('li', class_='lucky-work')
                    .find_all('img', class_='icon-work')
                )
                lucky_health = len(
                    seiza_box
                    .find('li', class_='lucky-health')
                    .find_all('img', class_='icon-health')
                )

                readings[zodiac_sign].update({
                    'forecast': forecast,
                    'key_of_fortune': key_of_fortune,
                    'lucky_color': lucky_color,
                    'lucky_money': lucky_money,
                    'lucky_love': lucky_love,
                    'lucky_work': lucky_work,
                    'lucky_health': lucky_health
                })
        except (AttributeError, TypeError):
            pass

        return readings
