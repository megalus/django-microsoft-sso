import importlib
from urllib.parse import urlparse

import httpx
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponseBase, HttpResponseRedirect
from django.shortcuts import resolve_url
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from loguru import logger

from django_microsoft_sso.main import MicrosoftAuth, UserHelper
from django_microsoft_sso.utils import send_message, show_credential


@require_http_methods(["GET"])
def start_login(request: HttpRequest) -> HttpResponseRedirect:
    auth = MicrosoftAuth(request)
    # Get the next url
    next_param = request.GET.get(key="next")
    if next_param:
        clean_param = (
            next_param
            if next_param.startswith("http") or next_param.startswith("/")
            else f"//{next_param}"
        )
    else:
        next_url = auth.get_sso_value("NEXT_URL")
        clean_param = reverse(next_url)
    next_path = urlparse(clean_param).path

    ms_auth = MicrosoftAuth(request)
    ms_auth.initiate()

    # Save data on Session
    if not request.session.session_key:
        request.session.create()
    timeout = auth.get_sso_value("TIMEOUT")
    request.session.set_expiry(timeout * 60)
    request.session["msal_graph_info"] = ms_auth.result
    request.session["sso_next_url"] = next_path
    request.session.save()

    # Redirect User
    return HttpResponseRedirect(ms_auth.get_auth_uri())


@require_http_methods(["GET"])
def callback(request: HttpRequest) -> HttpResponseRedirect:
    microsoft = MicrosoftAuth(request)
    login_failed_url = reverse(microsoft.get_sso_value("LOGIN_FAILED_URL"))
    code = request.GET.get("code")
    state = request.GET.get("state")

    next_url_from_session = request.session.get("sso_next_url")
    next_url_from_conf = reverse(microsoft.get_sso_value("next_url"))
    next_url = next_url_from_session if next_url_from_session else next_url_from_conf
    logger.debug(f"Next URL after login: {next_url}")

    # Check if Microsoft SSO is enabled
    enabled, message = microsoft.check_enabled(next_url)
    if not enabled:
        send_message(request, _(message))
        return HttpResponseRedirect(login_failed_url)

    # First, check for authorization code
    if not code:
        send_message(request, _("Authorization Code not received from SSO."))
        return HttpResponseRedirect(login_failed_url)

    # Then, check the state.
    request_state = request.session.get("msal_graph_info", {}).get("state")

    if not request_state or state != request_state:
        send_message(request, _("State Mismatch. Time expired?"))
        return HttpResponseRedirect(login_failed_url)

    # Get Access Token from Microsoft Graph
    auth_result = microsoft.get_user_token()
    if not auth_result:
        send_message(request, _("Access Token not received from SSO."))
        return HttpResponseRedirect(login_failed_url)
    if "error" in auth_result:
        send_message(
            request, _(f"Authorization Error received from SSO: {auth_result['error']}.")
        )
        if auth_result["error"] == "invalid_client":
            send_message(
                request, _("Please check your Client Credentials for MS Entra App.")
            )
            application_id = microsoft.get_sso_value("APPLICATION_ID")
            client_secret = microsoft.get_sso_value("CLIENT_SECRET")
            logger.debug(
                f"MICROSOFT_SSO_APPLICATION_ID: " f"{show_credential(application_id)}"
            )
            logger.debug(
                f"MICROSOFT_SSO_CLIENT_SECRET: " f"{show_credential(client_secret)}"
            )
        return HttpResponseRedirect(login_failed_url)

    try:
        user_result = microsoft.get_user_info()
    except Exception as error:
        send_message(request, _(f"Error while processing callback from SSO: {error}."))
        return HttpResponseRedirect(login_failed_url)

    user_helper = UserHelper(user_result, request)

    # Run Pre-Validate Callback
    pre_validate_callback = microsoft.get_sso_value("PRE_VALIDATE_CALLBACK")
    module_path = ".".join(pre_validate_callback.split(".")[:-1])
    pre_validate_fn = pre_validate_callback.split(".")[-1]
    module = importlib.import_module(module_path)
    user_is_valid = getattr(module, pre_validate_fn)(user_result, request)

    # Check if User Info is valid to login
    if not user_helper.email_is_valid or not user_is_valid:
        send_message(
            request,
            _(
                f"Email address not allowed: {user_helper.user_info_email}. "
                f"Please contact your administrator."
            ),
        )
        return HttpResponseRedirect(login_failed_url)

    # Add Access Token in Session
    if microsoft.get_sso_value("SAVE_ACCESS_TOKEN"):
        request.session["microsoft_sso_access_token"] = microsoft.token_info["access_token"]

    # Run Pre-Create Callback
    pre_create_callback = microsoft.get_sso_value("PRE_CREATE_CALLBACK")
    module_path = ".".join(pre_create_callback.split(".")[:-1])
    pre_login_fn = pre_create_callback.split(".")[-1]
    module = importlib.import_module(module_path)
    extra_users_args = getattr(module, pre_login_fn)(user_result, request)

    # Get or Create User
    auto_create_users = microsoft.get_sso_value("AUTO_CREATE_USERS")
    if auto_create_users:
        user = user_helper.get_or_create_user(extra_users_args)
    else:
        user = user_helper.find_user()

    if not user or not user.is_active:
        failed_login_message = (
            f"User not found - UPN: '{user_result['userPrincipalName']}', "
            f"Email: '{user_result['mail']}'"
        )
        if not user and not auto_create_users:
            failed_login_message += ". Auto-Create is disabled."

        if user and not user.is_active:
            failed_login_message = (
                f"User is not active: '{user_result['userPrincipalName']}'"
            )

        show_failed_login_message = microsoft.get_sso_value("SHOW_FAILED_LOGIN_MESSAGE")
        if show_failed_login_message:
            send_message(request, _(failed_login_message), level="warning")
        else:
            logger.warning(failed_login_message)

        return HttpResponseRedirect(login_failed_url)

    # Save Session
    request.session.save()

    # Run Pre-Login Callback
    pre_login_callback = microsoft.get_sso_value("PRE_LOGIN_CALLBACK")
    module_path = ".".join(pre_login_callback.split(".")[:-1])
    pre_login_fn = pre_login_callback.split(".")[-1]
    module = importlib.import_module(module_path)
    getattr(module, pre_login_fn)(user, request)

    # Get Authentication Backend
    # If exists, let's make a sanity check on it
    # Because Django does not raise errors if backend is wrong
    auth_backend = microsoft.get_sso_value("AUTHENTICATION_BACKEND")
    if auth_backend:
        module_path = ".".join(auth_backend.split(".")[:-1])
        backend_auth_class = auth_backend.split(".")[-1]
        try:
            module = importlib.import_module(module_path)
            getattr(module, backend_auth_class)
        except (ImportError, AttributeError) as error:
            raise ImportError(f"Authentication Backend invalid: {auth_backend}") from error

    # Login User
    login(request, user, auth_backend)

    session_cookie_age = microsoft.get_sso_value("SESSION_COOKIE_AGE")
    request.session.set_expiry(session_cookie_age)

    return HttpResponseRedirect(next_url)


@require_http_methods(["POST", "OPTIONS"])
def microsoft_slo_view(request: HttpRequest) -> HttpResponseBase:
    """
    Logout the User from Microsoft SSO and Django.

    Use this View for your logout URL.

    """
    # Logout from Microsoft
    auth = MicrosoftAuth(request)
    slo_enabled = auth.get_sso_value("SLO_ENABLED")
    sso_enabled = auth.get_sso_value("ENABLED")

    if slo_enabled and sso_enabled:
        microsoft = MicrosoftAuth(request)
        logout_redirect_path = auth.get_sso_value("LOGOUT_REDIRECT_PATH")
        homepage = resolve_url(logout_redirect_path)
        if not homepage.startswith("http"):
            homepage = request.build_absolute_uri(homepage)
        next_page = microsoft.get_logout_url(homepage=homepage)
        return LogoutView.as_view(next_page=next_page)(request)

    redirect_url = (
        reverse("admin:index")
        if request.path.startswith("admin:index")
        else reverse("index")
    )

    # Logout from Google (in case you're using both packages)
    token = request.session.get("google_sso_access_token")
    if token:
        httpx.post(
            "https://oauth2.googleapis.com/revoke", params={"token": token}, timeout=10
        )

    return LogoutView.as_view(next_page=redirect_url)(request)
