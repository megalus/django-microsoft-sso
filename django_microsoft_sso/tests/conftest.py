import importlib
from copy import deepcopy
from typing import Generator
from urllib.parse import quote, urlencode

import pytest
from django.apps import apps
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sites.models import Site
from django.db import connection, models
from django.test import AsyncClient
from django.urls import reverse

from django_microsoft_sso import conf
from django_microsoft_sso import conf as conf_module
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
    settings.MICROSOFT_SSO_PRE_LOGIN_CALLBACK = "django_microsoft_sso.hooks.pre_login_user"
    settings.MICROSOFT_SSO_PRE_CREATE_CALLBACK = (
        "django_microsoft_sso.hooks.pre_create_user"
    )
    settings.MICROSOFT_SSO_PRE_VALIDATE_CALLBACK = (
        "django_microsoft_sso.hooks.pre_validate_user"
    )
    settings.ALLOWED_HOSTS = ["testserver", "site.com", "other-site.com"]
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
def aclient_with_session(client_with_session, settings):
    """An alias for client_with_session to indicate async client usage."""
    settings.SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
    ac = AsyncClient()
    ac.cookies.update(client_with_session.cookies)
    return ac


@pytest.fixture
def callback_url(query_string):
    return f"{reverse('django_microsoft_sso:oauth_callback')}?{query_string}"


@pytest.fixture
def default_site(settings):
    site, _ = Site.objects.update_or_create(
        id=1, defaults={"domain": "site.com", "name": "Default Site"}
    )
    settings.SITE_ID = site.id
    return site


@pytest.fixture
def other_site(settings):
    site, _ = Site.objects.get_or_create(
        domain="other-site.com", defaults={"name": "Other Site"}
    )
    settings.SITE_ID = None
    return site


@pytest.fixture
def custom_user_model(settings) -> Generator[type, None, None]:
    """
    Create a temporary custom user model, point AUTH_USER_MODEL to it,
    recreate MicrosoftSSOUser table to reference the new model, yield the
    custom user class and then fully restore the previous state.
    """
    # Capture previous state
    old_auth = settings.AUTH_USER_MODEL
    import django_microsoft_sso.models as ms_models

    old_microsoftssouser = ms_models.MicrosoftSSOUser

    class CustomNamesUser(AbstractBaseUser):
        user_name = models.CharField(max_length=150, unique=True)
        mail = models.EmailField(unique=True)
        is_staff = models.BooleanField(default=False)
        is_active = models.BooleanField(default=True)

        USERNAME_FIELD = "user_name"
        EMAIL_FIELD = "mail"
        REQUIRED_FIELDS = ["mail"]

        class Meta:
            app_label = "django_microsoft_sso"

        def __str__(self) -> str:
            return self.user_name

    # Register dynamic model and create its table
    apps.register_model("django_microsoft_sso", CustomNamesUser)
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(CustomNamesUser)

    # Point to the new user model and reload conf + models so relations are rebuilt
    settings.AUTH_USER_MODEL = "django_microsoft_sso.CustomNamesUser"
    importlib.reload(conf_module)
    ms_models = importlib.reload(ms_models)

    # Replace MicrosoftSSOUser DB table so its FK points to the new user model
    new_microsoftssouser = ms_models.MicrosoftSSOUser
    with connection.schema_editor() as schema_editor:
        schema_editor.delete_model(old_microsoftssouser)
        schema_editor.create_model(new_microsoftssouser)

    importlib.reload(importlib.import_module("django_microsoft_sso.main"))

    try:
        yield CustomNamesUser
    finally:
        # Teardown: remove new tables and restore original model/table
        ms_models = importlib.reload(ms_models)
        new_microsoftssouser = ms_models.MicrosoftSSOUser

        with connection.schema_editor() as schema_editor:
            # delete the MicrosoftSSOUser table that references the dynamic user
            schema_editor.delete_model(new_microsoftssouser)
            # delete the dynamic user table
            schema_editor.delete_model(CustomNamesUser)

        # restore AUTH_USER_MODEL and reload modules
        settings.AUTH_USER_MODEL = old_auth
        importlib.reload(conf_module)
        importlib.reload(ms_models)

        # recreate the original MicrosoftSSOUser table created by migrations
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(old_microsoftssouser)

        # unregister the dynamic model from the apps registry and clear caches
        app_models = apps.all_models.get("django_microsoft_sso", {})
        app_models.pop("customnamesuser", None)
        apps.clear_cache()

        importlib.reload(importlib.import_module("django_microsoft_sso.main"))
