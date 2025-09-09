import uuid
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

import httpx
import msal
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Field, Q
from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from loguru import logger
from msal import ConfidentialClientApplication
from msal.authority import AuthorityBuilder

from django_microsoft_sso import conf
from django_microsoft_sso.models import MicrosoftSSOUser

STATE = str(uuid.uuid4())


@dataclass
class MicrosoftAuth:
    request: HttpRequest
    _auth: ConfidentialClientApplication = None
    result: dict[Any, Any] | None = None
    token_info: dict[Any, Any] | None = None

    def get_sso_value(self, key: str) -> Any:
        """Get SSO value from request or settings.

        Both configurations are valid:
        MICROSOFT_SSO_APPLICATION_ID = "your-client-id" # string value
        MICROSOFT_SSO_APPLICATION_ID = get_client_id # callable function

        When the value is a callable,
        it will be called with the request as an argument:

        def get_client_id(request):
            client_ids = {
                "example.com": "your-client-id",
                "other.com": "your-other-client-id",
            }
            return client_ids.get(request.site.domain, None)

        MICROSOFT_SSO_APPLICATION_ID = get_client_id

        :param key: The key to retrieve from the settings.
        :return: The value associated with the key.
        :raises ValueError: If the key is not found in the settings.
        """
        microsoft_sso_conf = f"MICROSOFT_SSO_{key.upper()}"
        if hasattr(conf, microsoft_sso_conf):
            value = getattr(conf, microsoft_sso_conf)
            if callable(value):
                logger.debug(
                    f"Value from conf {microsoft_sso_conf} is a callable. Calling it."
                )
                return value(self.request)
            return value
        raise ValueError(f"SSO Configuration '{microsoft_sso_conf}' not found in settings.")

    @property
    def scopes(self) -> list[str]:
        return self.get_sso_value("SCOPES")

    def get_netloc(self):
        callback_domain = self.get_sso_value("CALLBACK_DOMAIN")
        if callback_domain:
            logger.debug("Find Netloc using MICROSOFT_SSO_CALLBACK_DOMAIN")
            return callback_domain

        site = get_current_site(self.request)
        logger.debug("Find Netloc using Site domain")
        return site.domain

    def get_redirect_uri(self) -> str:
        if "HTTP_X_FORWARDED_PROTO" in self.request.META:
            scheme = self.request.META["HTTP_X_FORWARDED_PROTO"]
        else:
            scheme = self.request.scheme
        netloc = self.get_netloc()
        path = reverse("django_microsoft_sso:oauth_callback")
        callback_uri = f"{scheme}://{netloc}{path}"
        logger.debug(f"Callback URI: {callback_uri}")
        return callback_uri

    @property
    def auth(self) -> ConfidentialClientApplication:
        if not self._auth:
            authority = self.get_authority()
            self._auth = msal.ConfidentialClientApplication(
                client_id=self.get_sso_value("APPLICATION_ID"),
                client_credential=self.get_sso_value("CLIENT_SECRET"),
                authority=authority,
            )
        return self._auth

    def get_authority(self):
        authority = self.get_sso_value("AUTHORITY")
        if authority is None or isinstance(authority, AuthorityBuilder):
            return authority

        if not isinstance(authority, str):
            raise ValueError(
                "MICROSOFT_SSO_AUTHORITY must be a valid URL or an AuthorityBuilder object"
            )

        if isinstance(authority, str):
            data = urlparse(authority)
            if not data.scheme or not data.netloc:
                raise ValueError(
                    "MICROSOFT_SSO_AUTHORITY must be a valid URL "
                    "or an AuthorityBuilder object"
                )
        return authority

    def get_user_info(self):
        graph_url = "https://graph.microsoft.com/v1.0/me"
        token = self.token_info["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        graph_timeout = self.get_sso_value("GRAPH_TIMEOUT")
        response = httpx.get(graph_url, headers=headers, timeout=graph_timeout)
        user_info = response.json()
        response.raise_for_status()

        # Get Email Verified Flag
        graph_url = "https://graph.microsoft.com/v1.0/users/{}?$select=mailVerified".format(
            user_info["id"]
        )
        response = httpx.get(graph_url, headers=headers, timeout=graph_timeout)
        if response.status_code == 200:
            user_info.update({"email_verified": response.json().get("mailVerified", False)})

        # Get Picture Data
        graph_url = "https://graph.microsoft.com/v1.0/me/photo/$value"
        response = httpx.get(graph_url, headers=headers, timeout=graph_timeout)
        if response.status_code == 200:
            user_info.update({"picture_raw_data": response.content})

        return user_info

    def get_auth_uri(self):
        return self.result["auth_uri"]

    def get_user_token(self):
        request_params: dict[str, str] = {k: v for k, v in self.request.GET.items()}
        self.token_info = self.auth.acquire_token_by_auth_code_flow(
            auth_code_flow=self.request.session["msal_graph_info"],
            auth_response=request_params,
        )
        if "error_description" in self.token_info:
            error = self.token_info["error_description"]
            logger.error(f"Error acquiring token: {error}")
        return self.token_info

    def initiate(
        self, custom_scopes: list[str] | None = None, redirect_uri: str | None = None
    ) -> dict:
        self.result = self.auth.initiate_auth_code_flow(
            scopes=custom_scopes or self.get_sso_value("SCOPES"),
            redirect_uri=redirect_uri or self.get_redirect_uri(),
            state=STATE,
        )
        return self.result

    @staticmethod
    def get_logout_url(homepage):
        return (
            f"https://login.microsoftonline.com/common/oauth2/v2.0/"
            f"logout?post_logout_redirect_uri={homepage}"
        )

    def check_enabled(self, next_url: str) -> tuple[bool, str]:
        response = True, ""
        if not conf.MICROSOFT_SSO_ENABLED:
            response = False, "Microsoft SSO not enabled."
        else:
            admin_route = conf.SSO_ADMIN_ROUTE
            if callable(admin_route):
                admin_route = admin_route(self.request)

            admin_enabled = self.get_sso_value("admin_enabled")
            if admin_enabled is False and next_url.startswith(reverse(admin_route)):
                response = False, "Microsoft SSO not enabled for Admin."

            pages_enabled = self.get_sso_value("pages_enabled")
            if pages_enabled is False and not next_url.startswith(reverse(admin_route)):
                response = False, "Microsoft SSO not enabled for Pages."

        if response[1]:
            logger.debug(f"SSO Enable Check failed: {response[1]}")

        return response


@dataclass
class UserHelper:
    user_info: dict[Any, Any]
    request: Any
    user_changed: bool = False

    @property
    def user_info_email(self) -> str:
        user_email = self.user_info.get("mail") or ""
        return user_email.lower()  # Ensure email is lowercase

    @property
    def user_principal_name(self) -> str:
        return self.user_info["userPrincipalName"].lower()

    @property
    def user_model(self) -> type[User]:
        return get_user_model()

    @property
    def username_field(self) -> Field:
        return self.user_model._meta.get_field(self.user_model.USERNAME_FIELD)

    @property
    def email_field_name(self) -> str:
        return self.user_model.get_email_field_name()

    @property
    def email_is_valid(self) -> bool:
        auth = MicrosoftAuth(self.request)
        user_email_domain = self.user_info_email.split("@")[-1]
        allowable_domains = auth.get_sso_value("ALLOWABLE_DOMAINS")
        valid_domain = allowable_domains == ["*"]
        for email_domain in allowable_domains:
            if user_email_domain in email_domain:
                valid_domain = True
        email_verified = self.user_info.get("verified_email", None)
        if email_verified is not None and not email_verified:
            logger.debug(f"Email {self.user_info_email} is not verified.")
        return valid_domain

    def get_or_create_user(self, extra_users_args: dict | None = None):
        user_defaults = extra_users_args or {}

        auth = MicrosoftAuth(self.request)
        if auth.get_sso_value("UNIQUE_EMAIL"):
            if not self.user_info_email:
                raise ValueError("User email not found in Tenant data.")
            if self.username_field.name not in user_defaults:
                user_defaults[self.username_field.name] = self.user_principal_name

            user, created = self.user_model.objects.get_or_create(
                **{
                    f"{self.email_field_name}__iexact": self.user_info_email,
                    "defaults": user_defaults,
                }
            )
        else:
            user_defaults[self.email_field_name] = self.user_info_email

            # Find searching User Principal Name in MicrosoftSSOUser
            # For existing databases prior to this version, this field can be empty
            query = self.user_model.objects.filter(
                microsoftssouser__user_principal_name__iexact=self.user_principal_name
            )
            if query.exists():
                user = query.get()
                created = False
            else:
                username = user_defaults.pop(
                    self.username_field.name, self.user_principal_name
                )
                if self.email_field_name not in user_defaults:
                    user_defaults[self.email_field_name] = self.user_info_email
                if self.username_field.attname not in user_defaults:
                    user_defaults[self.username_field.attname] = username
                query = {
                    f"{self.username_field.attname}__iexact": username,
                    "defaults": user_defaults,
                }
                user, created = self.user_model.objects.get_or_create(**query)

        self.check_first_super_user(user)
        self.check_for_update(created, user)
        if self.user_changed:
            user.save()

        if auth.get_sso_value("SAVE_BASIC_MICROSOFT_INFO"):
            MicrosoftSSOUser.objects.update_or_create(
                user=user,
                defaults={
                    "microsoft_id": self.user_info["id"],
                    "picture_raw": self.user_info.get("picture_raw_data"),
                    "locale": self.user_info.get("preferredLanguage"),
                    "user_principal_name": self.user_principal_name,
                },
            )

        return user

    def check_for_update(self, created, user):
        auth = MicrosoftAuth(self.request)
        if created or auth.get_sso_value("ALWAYS_UPDATE_USER_DATA"):
            self.check_for_permissions(user)
            user.first_name = self.user_info.get("givenName") or ""
            user.last_name = self.user_info.get("surname") or ""
            setattr(user, self.email_field_name, self.user_info_email)
            user.set_unusable_password()
            self.user_changed = True

    def check_first_super_user(self, user):
        auth = MicrosoftAuth(self.request)
        if auth.get_sso_value("AUTO_CREATE_FIRST_SUPERUSER"):
            superuser_exists = self.user_model.objects.filter(is_superuser=True).exists()
            if not superuser_exists:
                message_text = _(
                    f"MICROSOFT_SSO_AUTO_CREATE_FIRST_SUPERUSER is True. "
                    f"Adding SuperUser status to email: {self.user_principal_name}"
                )
                messages.add_message(self.request, messages.INFO, message_text)
                logger.warning(message_text)
                user.is_superuser = True
                user.is_staff = True
                self.user_changed = True

    def check_for_permissions(self, user):
        user_email = getattr(user, self.email_field_name)
        auth = MicrosoftAuth(self.request)
        username = getattr(user, self.username_field.name, None)
        staff_list = auth.get_sso_value("STAFF_LIST")
        if user_email in staff_list or username in staff_list or "*" in staff_list:
            message_text = _(
                f"User: {self.user_principal_name} in MICROSOFT_SSO_STAFF_LIST. "
                f"Added Staff Permission."
            )
            messages.add_message(self.request, messages.INFO, message_text)
            logger.debug(message_text)
            user.is_staff = True

        superuser_list = auth.get_sso_value("SUPERUSER_LIST")
        if user_email in superuser_list or username in superuser_list:
            message_text = _(
                f"User: {self.user_principal_name} in MICROSOFT_SSO_SUPERUSER_LIST. "
                f"Added SuperUser Permission."
            )
            messages.add_message(self.request, messages.INFO, message_text)
            logger.debug(message_text)
            user.is_superuser = True
            user.is_staff = True

    def find_user(self):
        auth = MicrosoftAuth(self.request)
        if auth.get_sso_value("UNIQUE_EMAIL"):
            query = self.user_model.objects.filter(
                **{f"{self.email_field_name}__iexact": self.user_info_email}
            )
        else:
            username_query = {
                f"{self.username_field.attname}__iexact": self.user_principal_name
            }
            query = self.user_model.objects.filter(
                Q(microsoftssouser__user_principal_name__iexact=self.user_principal_name)
                | Q(**username_query)
            )
        return query.get() if query.exists() else None
