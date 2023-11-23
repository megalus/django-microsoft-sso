import importlib


def test_conf_from_settings(settings):
    # Arrange
    settings.MICROSOFT_SSO_ENABLED = False

    # Act
    from django_microsoft_sso import conf

    importlib.reload(conf)

    # Assert
    assert conf.MICROSOFT_SSO_ENABLED is False
