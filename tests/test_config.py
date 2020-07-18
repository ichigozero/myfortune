import filecmp


def test_export_config(tmp_path, config_path, app_config):
    tmp_config_path = tmp_path / 'myfortune.json'
    app_config._config_path = tmp_config_path
    app_config._config_values == {'foo': 'bar'}

    app_config.export_config()

    filecmp.cmp(tmp_config_path, config_path)


def test_import_config(config_path, app_config):
    app_config._config_path = config_path

    app_config.import_config()

    assert app_config._config_values == {'foo': 'bar'}
