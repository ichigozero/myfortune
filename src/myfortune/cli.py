import click

from .config import AppConfig
from .scraper import FujiTvScraper


@click.group()
def cmd():
    pass


@cmd.command()
def init_config():
    click.echo('Configuring SMTP settings:')

    app_config = AppConfig()
    app_config._config_values = {
        'smtp_username': click.prompt('Username', type=str),
        'stmp_password': click.prompt('Password', type=str),
        'smtp_address': click.prompt('SMTP Address', type=str),
        'encryption': click.prompt('Encryption', type=str, default='SSL'),
        'smtp_port': click.prompt('Port', type=int, default='465')
    }
    app_config.export_config()
    click.echo(
        'SMTP settings have been exported to '
        '{}'.format(app_config._config_path)
    )


@cmd.group()
def uranatte():
    pass


@uranatte.command()
@click.argument('birthdate')
def mezamashi(birthdate):
    scraper = FujiTvScraper()
    output_horoscope_readings(scraper, birthdate)


def output_horoscope_readings(scraper, birthdate):
    scraper.get_soup()
    scraper.extract_all_horoscope_readings()

    click.echo(scraper)
    filtered_readings = (
        scraper
        .filter_horoscope_readings(birthdate)
        .values()
    )
    for filtered_reading in filtered_readings:
        click.echo(filtered_reading)
