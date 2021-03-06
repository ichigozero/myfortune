import click

from .config import AppConfig
from .mailer import Mailer
from .scraper import FujiTvScraper
from .scraper import NipponTvScraper
from .scraper import TbsScraper
from .scraper import TvAsahiScraper


@click.group()
def cmd():
    pass


@cmd.command()
def init_config():
    click.echo('Configuring SMTP settings:')

    app_config = AppConfig()
    app_config.config_values = {}
    app_config.config_values['smtp'] = {
        'username': click.prompt('Username', type=str),
        'password': click.prompt('Password', type=str),
        'smtp_address': click.prompt('SMTP Address', type=str),
        'encryption': click.prompt('Encryption', type=str, default='SSL'),
        'port': click.prompt('Port', type=int, default='465')
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
@click.option('-e', '--email')
@click.argument('birthdate')
def mezamashi(email, birthdate):
    scraper = FujiTvScraper()
    output_horoscope_readings(scraper, birthdate, email)


@uranatte.command()
@click.option('-e', '--email')
@click.argument('birthdate')
def sukkirisu(email, birthdate):
    scraper = NipponTvScraper()
    output_horoscope_readings(scraper, birthdate, email)


@uranatte.command()
@click.option('-e', '--email')
@click.argument('birthdate')
def gudetama(email, birthdate):
    scraper = TbsScraper()
    output_horoscope_readings(scraper, birthdate, email)


@uranatte.command()
@click.option('-e', '--email')
@click.argument('birthdate')
def go_go_hoshi(email, birthdate):
    scraper = TvAsahiScraper()
    output_horoscope_readings(scraper, birthdate, email)


def output_horoscope_readings(scraper, birthdate, email):
    if email:
        send_horoscope_readings(scraper, birthdate, email)
    else:
        print_horoscope_readings(scraper, birthdate)


def print_horoscope_readings(scraper, birthdate):
    scraper.load_horoscope_readings_from_cache()

    if scraper._horoscope_readings == {}:
        scraper.get_soup()
        scraper.extract_all_horoscope_readings()
        scraper.cache_horoscope_readings()

    click.echo(scraper)
    filtered_readings = (
        scraper
        .filter_horoscope_readings(birthdate)
        .values()
    )
    for reading in filtered_readings:
        if reading:
            click.echo(reading)


def send_horoscope_readings(scraper, birthdate, email):
    app_config = AppConfig()
    app_config.import_config()

    scraper.load_horoscope_readings_from_cache()

    if scraper._horoscope_readings == {}:
        scraper.get_soup()
        scraper.extract_all_horoscope_readings()
        scraper.cache_horoscope_readings()

    filtered_readings = (
        scraper
        .filter_horoscope_readings(birthdate)
        .values()
    )
    recipients = [{
        'email': email,
        'subject': str(scraper),
        'message': '\n'.join([
            reading
            for reading in filtered_readings
            if reading
        ])
    }]

    mailer = Mailer(smtp_config=app_config.config_values['smtp'])
    mailer.send_mail(recipients)
