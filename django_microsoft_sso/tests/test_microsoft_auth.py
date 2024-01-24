import pytest
from django.contrib.sites.models import Site

from django_microsoft_sso import conf
from django_microsoft_sso.main import MicrosoftAuth

pytestmark = pytest.mark.django_db


def test_scopes(callback_request):
    # Arrange
    ms = MicrosoftAuth(callback_request)

    # Assert
    assert ms.scopes == conf.MICROSOFT_SSO_SCOPES


@pytest.mark.parametrize(
    "fixture, expected_scheme",
    [
        (pytest.lazy_fixture("callback_request"), "http"),
        (pytest.lazy_fixture("callback_request_from_reverse_proxy"), "https"),
    ],
)
def test_get_redirect_uri(fixture, expected_scheme, monkeypatch):
    # Arrange
    monkeypatch.setattr(conf, "MICROSOFT_SSO_CALLBACK_DOMAIN", None)
    current_site_domain = Site.objects.get_current().domain

    # Act
    ms = MicrosoftAuth(fixture)

    # Assert
    assert (
        ms.get_redirect_uri()
        == f"{expected_scheme}://{current_site_domain}/microsoft_sso/callback/"
    )


def test_redirect_uri_with_custom_domain(callback_request_from_reverse_proxy, monkeypatch):
    # Arrange
    monkeypatch.setattr(conf, "MICROSOFT_SSO_CALLBACK_DOMAIN", "my-other-domain.com")

    # Act
    ms = MicrosoftAuth(callback_request_from_reverse_proxy)

    # Assert
    assert ms.get_redirect_uri() == "https://my-other-domain.com/microsoft_sso/callback/"
