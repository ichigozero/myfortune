import click

from .config import AppConfig


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
