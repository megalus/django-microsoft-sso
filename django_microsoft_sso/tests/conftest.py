import importlib
from copy import deepcopy
from urllib.parse import quote, urlencode

import pytest
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse

from django_microsoft_sso import conf
from django_microsoft_sso.main import MicrosoftAuth

SECRET_PATH = "/secret/"


@pytest.fixture
def query_string():
    return urlencode(
        {
            "code": "12345",
            "state": "foo",
            "scope": " ".join(conf.MICROSOFT_SSO_SCOPES),
            "hd": "example.com",
            "prompt": "consent",
        },
        quote_via=quote,
    )


@pytest.fixture
def microsoft_response():
    return {
        "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#users/$entity",
        "businessPhones": [],
        "displayName": "Clark Kent",
        "givenName": "Clark",
        "jobTitle": None,
        "mail": "kalel@dailyplanet.com",
        "mobilePhone": None,
        "officeLocation": None,
        "preferredLanguage": "en-US",
        "surname": "Kent",
        "userPrincipalName": "kalel@dailyplanet.com",
        "id": "291azxdc-8e44-aa13-119b-60adddsss5e99",
        "picture_raw_data": b"foo",
        "verified_email": True,
    }


@pytest.fixture
def microsoft_response_update():
    return {
        "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#users/$entity",
        "businessPhones": [],
        "displayName": "Bruce Wayne",
        "givenName": "Bruce",
        "jobTitle": None,
        "mail": "kalel@dailyplanet.com",
        "mobilePhone": None,
        "officeLocation": None,
        "preferredLanguage": "en-US",
        "surname": "Wayne",
        "userPrincipalName": "kalel@dailyplanet.com",
        "id": "291azxdc-8e44-aa13-119b-60adddsss5e99",
        "picture_raw_data": b"foo",
        "verified_email": True,
    }


@pytest.fixture
def callback_request(rf, query_string):
    request = rf.get(f"/microsoft_sso/callback/?{query_string}")
    middleware = SessionMiddleware(get_response=lambda req: None)
    middleware.process_request(request)
    request.session.save()
    messages = FallbackStorage(request)
    setattr(request, "_messages", messages)
    return request


@pytest.fixture
def callback_request_from_reverse_proxy(rf, query_string):
    request = rf.get(
        f"/microsoft_sso/callback/?{query_string}", HTTP_X_FORWARDED_PROTO="https"
    )
    middleware = SessionMiddleware(get_response=lambda req: None)
    middleware.process_request(request)
    request.session.save()
    messages = FallbackStorage(request)
    setattr(request, "_messages", messages)
    return request


@pytest.fixture
def callback_request_with_state(callback_request):
    request = deepcopy(callback_request)
    request.session["msal_graph_info"] = {"state": "foo"}
    request.session["sso_next_url"] = "/secret/"
    return request


@pytest.fixture
def client_with_session(client, settings, mocker, microsoft_response):
    settings.MICROSOFT_SSO_ALLOWABLE_DOMAINS = ["example.com"]
    settings.MICROSOFT_SSO_PRE_LOGIN_CALLBACK = "django_google_sso.hooks.pre_login_user"
    importlib.reload(conf)
    session = client.session
    session.update({"msal_graph_info": {"state": "foo"}, "sso_next_url": SECRET_PATH})
    session.save()
    m = mocker.patch("django_microsoft_sso.main.ConfidentialClientApplication")
    m.acquire_token_by_auth_code_flow.return_value = {"access_token": "foo"}
    m.initiate_auth_code_flow.return_value = {"state": "foo"}
    mocker.patch.object(MicrosoftAuth, "auth", return_value=m)
    mocker.patch.object(MicrosoftAuth, "get_user_info", return_value=microsoft_response)
    yield client


@pytest.fixture
def callback_url(query_string):
    return f"{reverse('django_microsoft_sso:oauth_callback')}?{query_string}"
