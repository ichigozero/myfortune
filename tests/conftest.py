import os
import datetime

import pytest
from bs4 import BeautifulSoup

from myfortune import AppConfig
from myfortune import FujiTvScraper
from myfortune import Mailer
from myfortune import NipponTvScraper
from myfortune import Scraper
from myfortune import TbsScraper
from myfortune import TvAsahiScraper


def test_file(filename):
    path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'test_files',
    )
    with open(os.path.join(path, filename), 'r') as f:
        return f.read()


@pytest.fixture(scope='module')
def fake_datetime():
    return datetime.datetime(2020, 7, 17, 0, 0, 0)


@pytest.fixture(scope='module')
def fuji_tv_data():
    return test_file('fuji_tv.html').encode('utf-8')


@pytest.fixture(scope='module')
def nippon_tv_data():
    return test_file('nippon_tv.html').encode('utf-8')


@pytest.fixture(scope='module')
def tbs_data():
    return test_file('tbs.html').encode('utf-8')


@pytest.fixture(scope='module')
def tv_asahi_data():
    return test_file('tv_asahi.html').encode('utf-8')


@pytest.fixture(scope='module')
def config_path():
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'test_files',
        'myfortune.json'
    )


@pytest.fixture
def scraper():
    return Scraper()


@pytest.fixture
def fuji_tv_scraper(fuji_tv_data):
    scraper = FujiTvScraper()
    scraper._soup = BeautifulSoup(fuji_tv_data, 'html.parser')

    return scraper


@pytest.fixture
def nippon_tv_scraper(nippon_tv_data):
    scraper = NipponTvScraper()
    scraper._soup = BeautifulSoup(nippon_tv_data, 'html.parser')

    return scraper


@pytest.fixture
def tbs_scraper(tbs_data):
    scraper = TbsScraper()
    scraper._soup = BeautifulSoup(tbs_data, 'html.parser')

    return scraper


@pytest.fixture
def tv_asahi_scraper(tv_asahi_data):
    scraper = TvAsahiScraper()
    scraper._soup = BeautifulSoup(tv_asahi_data, 'html.parser')

    return scraper


@pytest.fixture
def app_config():
    return AppConfig()


@pytest.fixture
def mailer():
    smtp_config = {
        'login': 'login',
        'password': 'password',
        'encryption': 'SSL',
        'smtp': 'localhost',
        'port': 1025
    }
    return Mailer(smtp_config)
