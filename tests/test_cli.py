from click.testing import CliRunner

from myfortune import AppConfig
from myfortune import DEFAULT_CONFIG_PATH
from myfortune import FujiTvScraper
from myfortune import NipponTvScraper
from myfortune import TbsScraper
from myfortune import TvAsahiScraper
from myfortune import Mailer
from myfortune import go_go_hoshi
from myfortune import gudetama
from myfortune import init_config
from myfortune import mezamashi
from myfortune import sukkirisu


def test_init_config(mocker):
    export_config = mocker.patch.object(AppConfig, 'export_config')

    runner = CliRunner()
    result = runner.invoke(
        init_config,
        input=(
            'username\n'
            'password\n'
            'localhost\n'
            'SSL\n'
            '1025\n'
        )
    )

    export_config.assert_called_once()
    assert result.output == (
        'Configuring SMTP settings:\n'
        'Username: username\n'
        'Password: password\n'
        'SMTP Address: localhost\n'
        'Encryption [SSL]: SSL\n'
        'Port [465]: 1025\n'
        'SMTP settings have been exported to {}\n'.format(DEFAULT_CONFIG_PATH)
    )


def test_print_mezamashi_horoscope_readings(mocker):
    _test_print_horoscope_readings(
        mocker=mocker,
        command=mezamashi,
        title='めざまし占い',
        scraper=FujiTvScraper
    )


def test_print_sukkirisu_horoscope_readings(mocker):
    _test_print_horoscope_readings(
        mocker=mocker,
        command=sukkirisu,
        title='誕生月占い スッキリす！',
        scraper=NipponTvScraper
    )


def test_print_gudetama_horoscope_readings(mocker):
    _test_print_horoscope_readings(
        mocker=mocker,
        command=gudetama,
        title='ぐでたま占い',
        scraper=TbsScraper,
    )


def test_print_go_go_hoshi_horoscope_readings(mocker):
    _test_print_horoscope_readings(
        mocker=mocker,
        command=go_go_hoshi,
        title='ゴーゴー星占い',
        scraper=TvAsahiScraper,
    )


def _test_print_horoscope_readings(mocker, command, title, scraper):
    load_cache = mocker.patch.object(
        scraper,
        'load_horoscope_readings_from_cache'
    )
    get_soup = mocker.patch.object(scraper, 'get_soup')
    extract_readings = mocker.patch.object(
        scraper,
        'extract_all_horoscope_readings'
    )
    save_cache = mocker.patch.object(
        scraper,
        'cache_horoscope_readings'
    )
    filter_readings = mocker.patch.object(
        scraper,
        'filter_horoscope_readings',
        return_value={
            'rank': '1位',
            'forecast': '気合い充分で前進できるパワフル運勢！現状に',
            'advice_title': '★ラッキーポイント',
            'advice_description': '自分へのご褒美に買ったもの'
        }
    )

    runner = CliRunner()
    result = runner.invoke(command, ['1/21'])

    get_soup.assert_called_once()
    load_cache.assert_called_once()
    extract_readings.assert_called_once()
    save_cache.assert_called_once()
    filter_readings.assert_called_once()
    assert result.output == '\n'.join([
        title,
        '1位',
        '気合い充分で前進できるパワフル運勢！現状に',
        '★ラッキーポイント',
        '自分へのご褒美に買ったもの\n'
    ])


def test_send_mezamashi_horoscope_readings(mocker):
    _test_send_horoscope_readings(
        mocker=mocker,
        command=mezamashi,
        title='めざまし占い',
        scraper=FujiTvScraper
    )


def test_send_sukkirisu_horoscope_readings(mocker):
    _test_send_horoscope_readings(
        mocker=mocker,
        command=sukkirisu,
        title='誕生月占い スッキリす！',
        scraper=NipponTvScraper
    )


def test_send_gudetama_horoscope_readings(mocker):
    _test_send_horoscope_readings(
        mocker=mocker,
        command=gudetama,
        title='ぐでたま占い',
        scraper=TbsScraper,
    )


def test_send_go_go_hoshi_horoscope_readings(mocker):
    _test_send_horoscope_readings(
        mocker=mocker,
        command=go_go_hoshi,
        title='ゴーゴー星占い',
        scraper=TvAsahiScraper
    )


def _test_send_horoscope_readings(mocker, command, title, scraper):
    def _import_config(self):
        self.config_values = {
            'smtp': {
                'username': 'bar@localhost',
                'password': 'password',
                'encryption': 'SSL',
                'smtp_address': 'localhost',
                'port': 1025
            }
        }

    load_cache = mocker.patch.object(
        scraper,
        'load_horoscope_readings_from_cache'
    )
    get_soup = mocker.patch.object(scraper, 'get_soup')
    extract_readings = mocker.patch.object(
        scraper,
        'extract_all_horoscope_readings'
    )
    save_cache = mocker.patch.object(
        scraper,
        'cache_horoscope_readings'
    )
    filter_readings = mocker.patch.object(
        scraper,
        'filter_horoscope_readings',
        return_value={
            'rank': '1位',
            'forecast': '気合い充分で前進できるパワフル運勢！現状に',
            'advice_title': '★ラッキーポイント',
            'advice_description': '自分へのご褒美に買ったもの'
        }
    )
    import_config = mocker.patch.object(
        AppConfig,
        'import_config',
        side_effect=_import_config,
        autospec=True
    )
    send_mail = mocker.patch.object(Mailer, 'send_mail')

    runner = CliRunner()
    runner.invoke(command, ['--email', 'foo@localhost', '1/21'])

    load_cache.assert_called_once()
    get_soup.assert_called_once()
    extract_readings.assert_called_once()
    save_cache.assert_called_once()
    filter_readings.assert_called_once()
    import_config.assert_called_once()
    send_mail.assert_called_once_with([
        {
            'email': 'foo@localhost',
            'subject': title,
            'message': (
                '1位\n'
                '気合い充分で前進できるパワフル運勢！現状に\n'
                '★ラッキーポイント\n'
                '自分へのご褒美に買ったもの'
            )
        }
    ])
