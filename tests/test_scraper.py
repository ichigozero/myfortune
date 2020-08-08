import datetime
import os
import pickle
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


def test_cache_horoscope_readings(mocker, tmp_path, scraper):
    tmp_cache_path = str(tmp_path / 'file_20200717.pickle')
    mock_path = mocker.patch.object(
        scraper,
        '_construct_cache_file_path',
        return_value=tmp_cache_path
    )
    mock_open = mocker.patch(
        'builtins.open',
        mocker.mock_open()
    )
    spy_dump = mocker.spy(pickle, 'dump')

    scraper._horoscope_readings = {'foo': 'bar'}
    scraper.cache_horoscope_readings('')

    mock_path.assert_called_once()
    mock_open.assert_called_once_with(tmp_cache_path, 'wb')
    spy_dump.assert_called_once()


def test_load_horoscope_readings_from_cache(
        monkeypatch,
        dummy_cache,
        scraper
):
    def _mock_cache_file_path(*args, **kwargs):
        return dummy_cache

    monkeypatch.setattr(
        scraper,
        '_construct_cache_file_path',
        _mock_cache_file_path
    )
    scraper._horoscope_readings = None
    scraper.load_horoscope_readings_from_cache('')

    assert scraper._horoscope_readings == {'foo': 'bar'}


def test_construct_cache_path(
        monkeypatch,
        mocker,
        fake_datetime,
        tmp_path,
        scraper
):
    class MockDatetime:
        def today(*args, **kwargs):
            return fake_datetime

    monkeypatch.setattr(datetime, 'datetime', MockDatetime)
    mocker.patch(
        'appdirs.AppDirs.user_cache_dir',
        new_callable=mocker.PropertyMock,
        return_value=tmp_path
    )
    spy_makedirs = mocker.spy(os, 'makedirs')

    output = scraper._construct_cache_file_path('file')
    expected = os.path.join(tmp_path, 'file_20200717.pickle')

    spy_makedirs.assert_called_once_with(tmp_path, exist_ok=True)
    assert output == expected
