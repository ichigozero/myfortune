from click.testing import CliRunner

from myfortune import FujiTvScraper
from myfortune import mezamashi


def test_init_config(mocker):
    from myfortune import AppConfig
    from myfortune import DEFAULT_CONFIG_PATH
    from myfortune import init_config

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


def test_mezamashi(mocker):
    get_soup = mocker.patch.object(FujiTvScraper, 'get_soup')
    extract_readings = mocker.patch.object(
        FujiTvScraper,
        'extract_all_horoscope_readings'
    )
    filter_readings = mocker.patch.object(
        FujiTvScraper,
        'filter_horoscope_readings',
        return_value={
            'rank': '1位',
            'forecast': '気合い充分で前進できるパワフル運勢！現状に',
            'advice_title': '★ラッキーポイント',
            'advice_description': '自分へのご褒美に買ったもの'
        }
    )

    runner = CliRunner()
    result = runner.invoke(mezamashi, ['1/21'])

    get_soup.assert_called_once()
    extract_readings.assert_called_once()
    filter_readings.assert_called_once()
    assert result.output == (
        'めざまし占い\n'
        '1位\n'
        '気合い充分で前進できるパワフル運勢！現状に\n'
        '★ラッキーポイント\n'
        '自分へのご褒美に買ったもの\n'
    )
