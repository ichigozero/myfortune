import datetime
import pickle
import os
import re
import requests

from appdirs import AppDirs
from bs4 import BeautifulSoup

from .zodiac import Zodiac


class Scraper:
    def __init__(self):
        self._soup = None
        self._horoscope_readings = {}

    def get_soup(self, url):
        try:
            content = requests.get(url).content
            self._soup = BeautifulSoup(content, 'html.parser')
        except requests.exceptions.RequestException:
            pass

    def filter_horoscope_readings(self, birthdate):
        return self._horoscope_readings.get(Zodiac.get_zodiac_sign(birthdate))

    def cache_horoscope_readings(self, cache_title):
        cache_path = self._construct_cache_file_path(cache_title)

        with open(cache_path, 'wb') as file:
            pickle.dump(obj=self._horoscope_readings, file=file)

    def load_horoscope_readings_from_cache(self, cache_title):
        try:
            cache_path = self._construct_cache_file_path(cache_title)

            with open(cache_path, 'rb') as file:
                self._horoscope_readings = pickle.load(file)
        except OSError:
            pass

    def _construct_cache_file_path(self, cache_title):
        app_dirs = AppDirs(appname='myfortune')
        cache_filename = '{}_{}.pickle'.format(
            cache_title,
            datetime.datetime.today().strftime('%Y%m%d')
        )

        os.makedirs(app_dirs.user_cache_dir, exist_ok=True)

        return os.path.join(
            app_dirs.user_cache_dir,
            cache_filename
        )


FUJI_TV_URL = 'http://fcs2.sp2.fujitv.co.jp/fortune.php'


class FujiTvScraper(Scraper):
    def __str__(self):
        return 'めざまし占い'

    def get_soup(self):
        super().get_soup(FUJI_TV_URL)

    def extract_all_horoscope_readings(self):
        try:
            readings = {}
            rank_areas = self._soup.find_all('div', class_='rankArea')

            for rank_area in rank_areas:
                zodiac_sign = (
                    rank_area
                    .find('span', attrs={'class': None})
                    .get_text(strip=True)
                )
                rank = (
                    rank_area
                    .find('span', class_=re.compile('rank'))
                    .get_text(strip=True)
                )
                forecast = rank_area.section.p.get_text(strip=True)
                advice_section = rank_area.section.table.tr
                advice_title = (
                    advice_section
                    .find('th', id='starTitle')
                    .get_text(strip=True)
                )
                advice_description = (
                    rank_area
                    .section
                    .table
                    .td
                    .contents[0]
                    .strip()
                )

                readings[zodiac_sign] = {
                    'rank': rank,
                    'forecast': forecast,
                    'advice_title': '★{}'.format(advice_title),
                    'advice_description': advice_description
                }

            self._horoscope_readings.update(readings)
        except (AttributeError, TypeError):
            pass


NIPPON_TV_URL = 'https://www.ntv.co.jp/sukkiri/sukkirisu/'


class NipponTvScraper(Scraper):
    def __str__(self):
        return '誕生月占い スッキリす！'

    def get_soup(self):
        super().get_soup(NIPPON_TV_URL)

    def extract_all_horoscope_readings(self):
        try:
            readings = {}
            div_rows_1 = self._soup.find_all('div', class_='row1')
            div_rows_2 = self._soup.find_all('div', class_='row2')

            for index, div_row_1 in enumerate(div_rows_1):
                div_rank = div_row_1.find('div', class_='rank')

                if div_rank:
                    rank = int(
                        div_rank
                        .get_text(strip=True)
                        .replace('位', '')
                    )
                else:
                    if index == 10:
                        rank = 12
                    else:
                        rank = 1

                if rank == 1:
                    rank_group = (
                        self._soup
                        .find('h3', class_='rankGroup-1')
                        .get_text(strip=True)
                    )
                elif rank < 7:
                    rank_group = (
                        self._soup
                        .find('h3', class_='rankGroup-2')
                        .get_text(strip=True)
                    )
                elif rank < 11:
                    rank_group = (
                        self._soup
                        .find('h3', class_='rankGroup-7')
                        .get_text(strip=True)
                    )
                else:
                    rank_group = (
                        self._soup
                        .find('h3', class_='rankGroup-12')
                        .get_text(strip=True)
                    )

                month = int(
                    div_row_1
                    .find('p', class_='month')
                    .find('span')
                    .get_text(strip=True)
                )
                forecast = (
                    div_rows_2[index]
                    .find('p')
                    .get_text(strip=True)
                )
                lucky_color = (
                    div_rows_2[index]
                    .find('div')
                    .get_text(strip=True)
                )

                readings[month] = {
                    'rank': '{}位'.format(rank),
                    'rank_group': rank_group,
                    'forecast': forecast,
                    'lucky_color': ''.join([
                        'ラッキーカラー：',
                        lucky_color
                    ])
                }

            self._horoscope_readings.update(readings)
        except (AttributeError, TypeError):
            pass

    def filter_horoscope_readings(self, birthdate):
        parsed_birthdate = datetime.datetime.strptime(birthdate, '%m/%d')

        return self._horoscope_readings.get(parsed_birthdate.month)


TBS_URL = 'https://www.tbs.co.jp/hayadoki/gudetama/'
ZODIAC_SIGNS = {
    'ohitsuji': 'おひつじ座',
    'oushi': 'おうし座',
    'futago': 'ふたご座',
    'kani': 'かに座',
    'shishi': 'しし座',
    'otome': 'おとめ座',
    'tenbin': 'てんびん座',
    'sasori': 'さそり座',
    'ite': 'いて座',
    'yagi': 'やぎ座',
    'mizugame': 'みずがめ座',
    'uo': 'うお座'
}


class TbsScraper(Scraper):
    def __str__(self):
        return 'ぐでたま占い'

    def get_soup(self):
        super().get_soup(TBS_URL)

    def extract_all_horoscope_readings(self):
        def _extract_rank_title(div_class_name):
            return (
                self._soup
                .find('div', class_=div_class_name)
                .find('span')
                .get_text(strip=True)
            )

        try:
            readings = {}
            uranai_boxes = self._soup.find_all(
                'div',
                id=re.compile('^uranai_box*')
            )

            for uranai_box in uranai_boxes:
                zodiac_sign = ZODIAC_SIGNS.get(
                    uranai_box.find_all('span')[1].get('id'))
                rank = int(
                    uranai_box
                    .find('span', class_='alt')
                    .get_text(strip=True)
                    .replace('位', '')
                )

                if rank == 1:
                    rank_title = ''
                elif rank < 6:
                    rank_title = _extract_rank_title('mini_tit1')
                elif rank < 9:
                    rank_title = _extract_rank_title('mini_tit2')
                elif rank < 12:
                    rank_title = _extract_rank_title('mini_tit3')
                else:
                    rank_title = _extract_rank_title('mini_tit4')

                forecast = (
                    uranai_box
                    .find('p', class_='uranai_text')
                    .get_text(strip=True)
                )
                lucky_color = (
                    uranai_box
                    .find('span', class_='lucky_color')
                    .get_text(strip=True)
                    .replace(u'\xa0', u'')
                )
                lucky_item = (
                    uranai_box
                    .find('span', class_='lucky_item')
                    .get_text(strip=True)
                    .replace(u'\xa0', u'')
                )

                p_tag = uranai_box.find('p', class_='advice_text')
                if p_tag:
                    advice = p_tag.get_text(strip=True)
                else:
                    advice = ''

                readings[zodiac_sign] = {
                    'rank': '{}位'.format(rank),
                    'rank_title': rank_title,
                    'forecast': forecast,
                    'lucky_color': lucky_color,
                    'lucky_item': lucky_item,
                    'advice': advice
                }

            self._horoscope_readings = readings
        except (AttributeError, TypeError):
            pass


TV_ASAHI_URL = 'https://www.tv-asahi.co.jp/goodmorning/uranai/'


class TvAsahiScraper(Scraper):
    def __str__(self):
        return 'ゴーゴー星占い'

    def get_soup(self):
        super().get_soup(TV_ASAHI_URL)

    def extract_all_horoscope_readings(self):
        try:
            readings = {}
            rank_box = self._soup.find('ul', class_='rank-box')
            li_tags = rank_box.find_all('li')

            for rank_index, li_tag in enumerate(li_tags, start=1):
                zodiac_sign = li_tag.find('span').get_text(strip=True)
                readings[zodiac_sign] = {'rank': '{}位'.format(rank_index)}

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

                lucky_color_text = (
                    seiza_box
                    .find('span', class_='lucky-color-txt')
                )
                lucky_color = ''.join([
                    lucky_color_text.get_text(strip=True),
                    lucky_color_text.next_sibling.strip()
                ])

                key_of_fortune_text = (
                    seiza_box
                    .find('span', class_='key-txt')
                )
                key_of_fortune = ''.join([
                    key_of_fortune_text.get_text(strip=True),
                    key_of_fortune_text.next_sibling.strip()
                ])

                lucky_money_count = len(
                    seiza_box
                    .find('li', class_='lucky-money')
                    .find_all('img', class_='icon-money')
                )
                lucky_love_count = len(
                    seiza_box
                    .find('li', class_='lucky-love')
                    .find_all('img', class_='icon-love')
                )
                lucky_work_count = len(
                    seiza_box
                    .find('li', class_='lucky-work')
                    .find_all('img', class_='icon-work')
                )
                lucky_health_count = len(
                    seiza_box
                    .find('li', class_='lucky-health')
                    .find_all('img', class_='icon-health')
                )

                readings[zodiac_sign].update({
                    'forecast': forecast,
                    'lucky_color': lucky_color,
                    'key_of_fortune': key_of_fortune,
                    'lucky_money': ''.join([
                        '金運：',
                        '★' * lucky_money_count
                    ]),
                    'lucky_love': ''.join([
                        '恋愛運：',
                        '★' * lucky_love_count
                    ]),
                    'lucky_work': ''.join([
                        '仕事運：',
                        '★' * lucky_work_count
                    ]),
                    'lucky_health': ''.join([
                        '健康運：',
                        '★' * lucky_health_count
                    ])
                })

            self._horoscope_readings = readings
        except (AttributeError, TypeError):
            pass
