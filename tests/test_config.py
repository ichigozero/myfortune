def test_import_config(config_path, app_config):
    app_config._config_path = config_path

    app_config.import_config()

    assert app_config._config_values == {'foo': 'bar'}
