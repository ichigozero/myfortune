import filecmp
import logging

import pytest


def test_export_config(tmp_path, config_path, app_config):
    tmp_config_path = tmp_path / 'myfortune.json'
    app_config._config_path = tmp_config_path
    app_config.config_values == {'foo': 'bar'}

    app_config.export_config()

    filecmp.cmp(tmp_config_path, config_path)


def test_import_config(config_path, app_config):
    app_config._config_path = config_path

    app_config.import_config()

    assert app_config.config_values == {'foo': 'bar'}


def test_failed_to_import_config(tmp_path, caplog, app_config):
    tmp_config_path = tmp_path / 'myfortune.json'
    app_config._config_path = tmp_config_path

    caplog.set_level(logging.ERROR)

    with pytest.raises(SystemExit) as exception:
        app_config.import_config()

    assert pytest.raises(FileNotFoundError)
    assert 'Config file not found: {}'.format(tmp_config_path) in caplog.text
    assert exception.value.code == 1
