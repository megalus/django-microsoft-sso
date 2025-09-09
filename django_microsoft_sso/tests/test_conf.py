import pytest

from django_microsoft_sso import conf

pytestmark = pytest.mark.django_db


def test_conf_from_settings(settings):
    # Arrange
    settings.MICROSOFT_SSO_ENABLED = False
    # Assert
    assert conf.MICROSOFT_SSO_ENABLED is False
