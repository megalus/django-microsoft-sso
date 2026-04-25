import pytest
from django.contrib.sites.models import Site
from msal.authority import AZURE_PUBLIC, AuthorityBuilder

from django_microsoft_sso import conf
from django_microsoft_sso.main import MicrosoftAuth

pytestmark = pytest.mark.django_db


def test_scopes(callback_request):
    # Arrange
    ms = MicrosoftAuth(callback_request)

    # Assert
    assert ms.scopes == conf.MICROSOFT_SSO_SCOPES


def test_get_redirect_uri_with_http(callback_request, monkeypatch):
    # Arrange
    expected_scheme = "http"
    monkeypatch.setattr(conf, "MICROSOFT_SSO_CALLBACK_DOMAIN", None)
    current_site_domain = Site.objects.get_current().domain

    # Act
    ms = MicrosoftAuth(callback_request)

    # Assert
    assert (
        ms.get_redirect_uri()
        == f"{expected_scheme}://{current_site_domain}/microsoft_sso/callback/"
    )


def test_get_redirect_uri_with_reverse_proxy(
    callback_request_from_reverse_proxy, monkeypatch
):
    # Arrange
    expected_scheme = "https"
    monkeypatch.setattr(conf, "MICROSOFT_SSO_CALLBACK_DOMAIN", None)
    current_site_domain = Site.objects.get_current().domain

    # Act
    ms = MicrosoftAuth(callback_request_from_reverse_proxy)

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


@pytest.mark.parametrize(
    "data, expect_raise",
    [
        ("https://login.microsoftonline.com/contoso", False),
        (AuthorityBuilder(AZURE_PUBLIC, "contoso.onmicrosoft.com"), False),
        (None, False),
        ("contoso", True),
    ],
)
def test_custom_authorities(
    data, expect_raise, callback_request_from_reverse_proxy, monkeypatch
):
    # Arrange
    monkeypatch.setattr(conf, "MICROSOFT_SSO_AUTHORITY", data)

    # Act
    ms = MicrosoftAuth(callback_request_from_reverse_proxy)

    # Assert
    if expect_raise:
        with pytest.raises(ValueError):
            ms.get_authority()
    else:
        assert ms.get_authority() == data


def test_get_redirect_uri_from_multiple_reverse_proxies(rf, query_string, monkeypatch):
    # Arrange
    expected_scheme = "https"
    monkeypatch.setattr(conf, "MICROSOFT_SSO_CALLBACK_DOMAIN", None)
    current_site_domain = Site.objects.get_current().domain
    request = rf.get(
        f"/microsoft_sso/callback/?{query_string}",
        HTTP_X_FORWARDED_PROTO="https, https",
    )

    # Act
    ms = MicrosoftAuth(request)

    # Assert
    assert (
        ms.get_redirect_uri()
        == f"{expected_scheme}://{current_site_domain}/microsoft_sso/callback/"
    )


def test_initiate_uses_get_by_default(callback_request, settings, mocker):
    # Arrange
    settings.MICROSOFT_SSO_REQUIRE_SECURE_CALLBACK = False
    flow_mock = mocker.patch.object(MicrosoftAuth, "auth")
    flow_mock.initiate_auth_code_flow.return_value = {
        "state": "foo",
        "auth_uri": "https://foo/bar",
    }
    ms = MicrosoftAuth(callback_request)

    # Act
    ms.initiate()

    # Assert
    flow_mock.initiate_auth_code_flow.assert_called_once()
    call_kwargs = flow_mock.initiate_auth_code_flow.call_args.kwargs
    assert call_kwargs["response_mode"] == "query"


def test_initiate_secure_uses_post_when_caches_is_configured(
    callback_request, settings, mocker
):
    # Arrange
    settings.MICROSOFT_SSO_REQUIRE_SECURE_CALLBACK = True
    settings.CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    }
    flow_mock = mocker.patch.object(MicrosoftAuth, "auth")
    flow_mock.initiate_auth_code_flow.return_value = {
        "state": "foo",
        "auth_uri": "https://foo/bar",
    }
    ms = MicrosoftAuth(callback_request)

    # Act
    ms.initiate()

    # Assert
    flow_mock.initiate_auth_code_flow.assert_called_once()
    call_kwargs = flow_mock.initiate_auth_code_flow.call_args.kwargs
    assert call_kwargs["response_mode"] == "form_post"
