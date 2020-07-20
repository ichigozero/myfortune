import requests

from bs4 import BeautifulSoup

from myfortune import Zodiac

DUMMY_URL = 'http://localhost'


def test_get_soup(requests_mock, scraper, tv_asahi_data):
    requests_mock.get(DUMMY_URL, content=tv_asahi_data)
    scraper.get_soup(DUMMY_URL)
    assert scraper._soup == BeautifulSoup(tv_asahi_data, 'html.parser')


def test_failed_to_get_soup(requests_mock, scraper):
    requests_mock.get(DUMMY_URL, exc=requests.exceptions.HTTPError)
    scraper.get_soup(DUMMY_URL)
    assert scraper._soup is None


def test_filter_horoscope_readings(mocker, scraper):
    mocker.patch.object(Zodiac, 'get_zodiac_sign', return_value='おひつじ座')
    scraper._horoscope_readings = {'おひつじ座': 'foo'}

    assert scraper.filter_horoscope_readings('4/1') == 'foo'
