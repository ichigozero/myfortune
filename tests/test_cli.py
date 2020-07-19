from click.testing import CliRunner

from myfortune import init_config


def test_init_config(mocker):
    from myfortune import AppConfig
    from myfortune import DEFAULT_CONFIG_PATH

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
