import os

import pytest

from myfortune import Scraper


def test_file(filename):
    path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'test_files',
    )
    with open(os.path.join(path, filename), 'r') as f:
        return f.read()


@pytest.fixture(scope='module')
def tv_asahi_data():
    return test_file('tv_asahi.html').encode('utf-8')


@pytest.fixture
def scraper():
    return Scraper()
