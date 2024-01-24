import importlib
from urllib.parse import urlparse

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from django_microsoft_sso import conf
from django_microsoft_sso.main import MicrosoftAuth, UserHelper


@require_http_methods(["GET"])
def start_login(request: HttpRequest) -> HttpResponseRedirect:
    # Get the next url
    next_param = request.GET.get(key="next")
    if next_param:
        clean_param = (
            next_param
            if next_param.startswith("http") or next_param.startswith("/")
            else f"//{next_param}"
        )
    else:
        clean_param = reverse(conf.MICROSOFT_SSO_NEXT_URL)
    next_path = urlparse(clean_param).path

    ms_auth = MicrosoftAuth(request)
    ms_auth.initiate()

    # Save data on Session
    if not request.session.session_key:
        request.session.create()
    request.session.set_expiry(conf.MICROSOFT_SSO_TIMEOUT * 60)
    request.session["msal_graph_info"] = ms_auth.result
    request.session["sso_next_url"] = next_path
    request.session.save()

    # Redirect User
    return HttpResponseRedirect(ms_auth.get_auth_uri())


@require_http_methods(["GET"])
def callback(request: HttpRequest) -> HttpResponseRedirect:
    login_failed_url = reverse(conf.MICROSOFT_SSO_LOGIN_FAILED_URL)
    microsoft = MicrosoftAuth(request)
    code = request.GET.get("code")
    state = request.GET.get("state")

    # Check if Microsoft SSO is enabled
    if not conf.MICROSOFT_SSO_ENABLED:
        messages.add_message(request, messages.ERROR, _("Microsoft SSO not enabled."))
        return HttpResponseRedirect(login_failed_url)

    # First, check for authorization code
    if not code:
        messages.add_message(
            request, messages.ERROR, _("Authorization Code not received from SSO.")
        )
        return HttpResponseRedirect(login_failed_url)

    # Then, check the state.
    request_state = request.session.get("msal_graph_info", {}).get("state")
    next_url = request.session.get("sso_next_url")

    if not request_state or state != request_state:
        messages.add_message(request, messages.ERROR, _("State Mismatch. Time expired?"))
        return HttpResponseRedirect(login_failed_url)

    # Get Access Token from Microsoft Graph
    auth_result = microsoft.get_user_token()
    if not auth_result:
        messages.add_message(
            request, messages.ERROR, _("Authorization Data not received from SSO.")
        )
        return HttpResponseRedirect(login_failed_url)
    if "error" in auth_result:
        messages.add_message(
            request,
            messages.ERROR,
            _(f"Authorization Error received from SSO: {auth_result['error']}."),
        )
        if auth_result["error"] == "invalid_client":
            messages.add_message(
                request,
                messages.ERROR,
                _("Please check your Client Credentials for MS Entra App."),
            )
        return HttpResponseRedirect(login_failed_url)

    try:
        user_result = microsoft.get_user_info()
    except Exception as error:
        messages.add_message(request, messages.ERROR, str(error))
        return HttpResponseRedirect(login_failed_url)

    user_helper = UserHelper(user_result, request)

    # Check if User Info is valid to login
    if not user_helper.email_is_valid:
        messages.add_message(
            request,
            messages.ERROR,
            _(
                f"Email address not allowed: {user_helper.user_email}. "
                f"Please contact your administrator."
            ),
        )
        return HttpResponseRedirect(login_failed_url)

    # Get or Create User
    if conf.MICROSOFT_SSO_AUTO_CREATE_USERS:
        user = user_helper.get_or_create_user()
    else:
        user = user_helper.find_user()

    if not user or not user.is_active:
        return HttpResponseRedirect(login_failed_url)

    # Add Access Token in Session
    if conf.MICROSOFT_SSO_SAVE_ACCESS_TOKEN:
        request.session["microsoft_sso_access_token"] = microsoft.token_info["access_token"]

    # Save Session
    request.session.save()

    # Run Pre-Login Callback
    module_path = ".".join(conf.MICROSOFT_SSO_PRE_LOGIN_CALLBACK.split(".")[:-1])
    pre_login_fn = conf.MICROSOFT_SSO_PRE_LOGIN_CALLBACK.split(".")[-1]
    module = importlib.import_module(module_path)
    getattr(module, pre_login_fn)(user, request)

    # Login User
    login(request, user, conf.MICROSOFT_SSO_AUTHENTICATION_BACKEND)
    request.session.set_expiry(conf.MICROSOFT_SSO_SESSION_COOKIE_AGE)

    return HttpResponseRedirect(next_url or reverse(conf.MICROSOFT_SSO_NEXT_URL))


@require_http_methods(["POST", "OPTIONS"])
def microsoft_slo_view(request: HttpRequest) -> TemplateResponse:
    """
    Logout the User from Microsoft SSO and Django.

    Use this View for your logout URL.

    """

    if conf.MICROSOFT_SLO_ENABLED and conf.MICROSOFT_SSO_ENABLED:
        microsoft = MicrosoftAuth(request)
        homepage = resolve_url(
            conf.MICROSOFT_SSO_LOGOUT_REDIRECT_PATH
        )  # Default: "admin:index"
        if not homepage.startswith("http"):
            homepage = request.build_absolute_uri(homepage)
        next_page = microsoft.get_logout_url(homepage=homepage)
        return LogoutView.as_view(next_page=next_page)(request)
    return LogoutView.as_view()(request)
