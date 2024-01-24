import importlib

import pytest
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.urls import reverse

from django_microsoft_sso import conf
from django_microsoft_sso.main import MicrosoftAuth
from django_microsoft_sso.tests.conftest import SECRET_PATH

ROUTE_NAME = "django_microsoft_sso:oauth_callback"


pytestmark = pytest.mark.django_db()


class MyBackend(ModelBackend):
    """Simple test for custom authentication backend"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        return super().authenticate(request, username, password, **kwargs)


def test_start_login(client, mocker):
    # Arrange
    flow_mock = mocker.patch.object(MicrosoftAuth, "auth")
    flow_mock.initiate_auth_code_flow.return_value = {
        "state": "foo",
        "auth_uri": "https://foo/bar",
    }

    # Act
    url = reverse("django_microsoft_sso:oauth_start_login") + "?next=/secret/"
    response = client.get(url)

    # Assert
    assert response.status_code == 302
    assert client.session["sso_next_url"] == SECRET_PATH


def test_start_login_none_next_param(client, mocker):
    # Arrange
    flow_mock = mocker.patch.object(MicrosoftAuth, "auth")
    flow_mock.initiate_auth_code_flow.return_value = {
        "state": "foo",
        "auth_uri": "https://foo/bar",
    }

    # Act
    url = reverse("django_microsoft_sso:oauth_start_login")
    response = client.get(url)

    # Assert
    assert response.status_code == 302
    assert client.session["sso_next_url"] == reverse(conf.MICROSOFT_SSO_NEXT_URL)


@pytest.mark.parametrize(
    "test_parameter",
    [
        "bad-domain.com/secret/",
        "www.bad-domain.com/secret/",
        "//bad-domain.com/secret/",
        "http://bad-domain.com/secret/",
        "https://malicious.example.com/secret/",
    ],
)
def test_exploit_redirect(client, mocker, test_parameter):
    # Arrange
    flow_mock = mocker.patch.object(MicrosoftAuth, "auth")
    flow_mock.initiate_auth_code_flow.return_value = {
        "state": "foo",
        "auth_uri": "https://foo/bar",
    }

    # Act
    url = reverse("django_microsoft_sso:oauth_start_login") + f"?next={test_parameter}"
    response = client.get(url)

    # Assert
    assert response.status_code == 302
    assert client.session["sso_next_url"] == SECRET_PATH


def test_microsoft_sso_disabled(settings, client):
    # Arrange
    from django_microsoft_sso import conf

    settings.MICROSOFT_SSO_ENABLED = False
    importlib.reload(conf)

    # Act
    response = client.get(reverse(ROUTE_NAME))

    # Assert
    assert response.status_code == 302
    assert User.objects.count() == 0
    assert "Microsoft SSO not enabled." in [
        m.message for m in get_messages(response.wsgi_request)
    ]


def test_missing_code(client):
    # Arrange
    importlib.reload(conf)

    # Act
    response = client.get(reverse(ROUTE_NAME))

    # Assert
    assert response.status_code == 302
    assert User.objects.count() == 0
    assert "Authorization Code not received from SSO." in [
        m.message for m in get_messages(response.wsgi_request)
    ]


@pytest.mark.parametrize("querystring", ["?code=1234", "?code=1234&state=bad_dog"])
def test_bad_state(client, querystring):
    # Arrange
    importlib.reload(conf)
    session = client.session
    session.update({"sso_state": "good_dog"})
    session.save()

    # Act
    url = reverse(ROUTE_NAME) + querystring
    response = client.get(url)

    # Assert
    assert response.status_code == 302
    assert User.objects.count() == 0
    assert "State Mismatch. Time expired?" in [
        m.message for m in get_messages(response.wsgi_request)
    ]


def test_invalid_email(client_with_session, settings, callback_url, microsoft_response):
    # Arrange
    from django_microsoft_sso import conf

    settings.MICROSOFT_SSO_ALLOWABLE_DOMAINS = ["foobar.com"]
    importlib.reload(conf)

    # Act
    response = client_with_session.get(callback_url)

    # Assert
    assert response.status_code == 302
    assert User.objects.count() == 0
    assert (
        f"Email address not allowed: {microsoft_response['mail']}. "
        f"Please contact your administrator."
        in [m.message for m in get_messages(response.wsgi_request)]
    )


def test_inactive_user(client_with_session, callback_url, microsoft_response):
    # Arrange
    User.objects.create(
        username=microsoft_response["mail"],
        email=microsoft_response["mail"],
        is_active=False,
    )

    # Act
    response = client_with_session.get(callback_url)

    # Assert
    assert response.status_code == 302
    assert User.objects.count() == 1
    assert User.objects.get(email=microsoft_response["mail"]).is_active is False


def test_new_user_login(client_with_session, callback_url, settings, mocker):
    # Arrange
    flow_mock = mocker.patch.object(MicrosoftAuth, "auth")
    flow_mock.acquire_token_by_auth_code_flow.return_value = {"access_token": "foo"}
    User.objects.all().delete()
    assert User.objects.count() == 0
    settings.MICROSOFT_SSO_ALLOWABLE_DOMAINS = ["dailyplanet.com"]
    importlib.reload(conf)

    # Act
    response = client_with_session.get(callback_url)

    # Assert
    assert response.status_code == 302
    assert User.objects.count() == 1
    assert response.url == SECRET_PATH
    assert response.wsgi_request.user.is_authenticated is True


def test_existing_user_login(
    client_with_session, settings, microsoft_response, callback_url, mocker
):
    # Arrange
    from django_microsoft_sso import conf

    flow_mock = mocker.patch.object(MicrosoftAuth, "auth")
    flow_mock.acquire_token_by_auth_code_flow.return_value = {"access_token": "foo"}

    existing_user = User.objects.create(
        username=microsoft_response["mail"],
        email=microsoft_response["mail"],
        is_active=True,
    )

    settings.MICROSOFT_SSO_ALLOWABLE_DOMAINS = ["dailyplanet.com"]
    settings.MICROSOFT_SSO_AUTO_CREATE_USERS = False
    importlib.reload(conf)

    # Act
    response = client_with_session.get(callback_url)

    # Assert
    assert response.status_code == 302
    assert User.objects.count() == 1
    assert response.url == SECRET_PATH
    assert response.wsgi_request.user.is_authenticated is True
    assert response.wsgi_request.user.email == existing_user.email


def test_missing_user_login(client_with_session, settings, callback_url):
    # Arrange
    from django_microsoft_sso import conf

    settings.MICROSOFT_SSO_AUTO_CREATE_USERS = False
    importlib.reload(conf)

    # Act
    response = client_with_session.get(callback_url)

    # Assert
    assert response.status_code == 302
    assert User.objects.count() == 0
    assert response.url == "/admin/"
    assert response.wsgi_request.user.is_authenticated is False
