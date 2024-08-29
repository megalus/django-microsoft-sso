import uuid
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

import httpx
import msal
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Field, Model, Q
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

    @property
    def scopes(self) -> list[str]:
        return conf.MICROSOFT_SSO_SCOPES

    def get_netloc(self):
        if conf.MICROSOFT_SSO_CALLBACK_DOMAIN:
            logger.debug("Find Netloc using MICROSOFT_SSO_CALLBACK_DOMAIN")
            return conf.MICROSOFT_SSO_CALLBACK_DOMAIN

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
                client_id=conf.MICROSOFT_SSO_APPLICATION_ID,
                client_credential=conf.MICROSOFT_SSO_CLIENT_SECRET,
                authority=authority,
            )
        return self._auth

    @staticmethod
    def get_authority():
        if conf.MICROSOFT_SSO_AUTHORITY is None or isinstance(
            conf.MICROSOFT_SSO_AUTHORITY, AuthorityBuilder
        ):
            return conf.MICROSOFT_SSO_AUTHORITY

        authority_value = conf.MICROSOFT_SSO_AUTHORITY
        if not isinstance(authority_value, str):
            raise ValueError(
                "MICROSOFT_SSO_AUTHORITY must be a valid URL or an AuthorityBuilder object"
            )

        if isinstance(authority_value, str):
            data = urlparse(authority_value)
            if not data.scheme or not data.netloc:
                raise ValueError(
                    "MICROSOFT_SSO_AUTHORITY must be a valid URL "
                    "or an AuthorityBuilder object"
                )
        return authority_value

    def get_user_info(self):
        graph_url = "https://graph.microsoft.com/v1.0/me"
        token = self.token_info["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        response = httpx.get(graph_url, headers=headers)
        user_info = response.json()
        response.raise_for_status()

        # Get Email Verified Flag
        graph_url = "https://graph.microsoft.com/v1.0/users/{}?$select=mailVerified".format(
            user_info["id"]
        )
        response = httpx.get(graph_url, headers=headers)
        if response.status_code == 200:
            user_info.update({"email_verified": response.json().get("mailVerified", False)})

        # Get Picture Data
        graph_url = "https://graph.microsoft.com/v1.0/me/photo/$value"
        response = httpx.get(graph_url, headers=headers)
        if response.status_code == 200:
            user_info.update({"picture_raw_data": response.content})

        return user_info

    def get_auth_uri(self):
        return self.result["auth_uri"]

    def get_user_token(self):
        self.token_info = self.auth.acquire_token_by_auth_code_flow(
            auth_code_flow=self.request.session["msal_graph_info"],
            auth_response={
                "code": self.request.GET.get("code"),
                "state": self.request.GET.get("state"),
                "session_state": self.request.GET.get("session_state"),
            },
        )
        return self.token_info

    def initiate(
        self, custom_scopes: list[str] | None = None, redirect_uri: str | None = None
    ) -> dict:
        self.result = self.auth.initiate_auth_code_flow(
            scopes=custom_scopes or settings.MICROSOFT_SSO_SCOPES,
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


@dataclass
class UserHelper:
    user_info: dict[Any, Any]
    request: Any
    user_changed: bool = False

    @property
    def user_email(self) -> str:
        user_email = self.user_info.get("mail") or ""
        return user_email.lower()  # Ensure email is lowercase

    @property
    def user_principal_name(self) -> str:
        return self.user_info["userPrincipalName"].lower()

    @property
    def user_model(self) -> AbstractUser | Model:
        return get_user_model()

    @property
    def username_field(self) -> Field:
        return self.user_model._meta.get_field(self.user_model.USERNAME_FIELD)

    @property
    def email_is_valid(self) -> bool:
        user_email_domain = self.user_email.split("@")[-1]
        valid_domain = False
        for email_domain in conf.MICROSOFT_SSO_ALLOWABLE_DOMAINS:
            if user_email_domain in email_domain:
                valid_domain = True
        email_verified = self.user_info.get("verified_email", None)
        if email_verified is not None and not email_verified:
            logger.debug(f"Email {self.user_email} is not verified.")
        return valid_domain

    def get_or_create_user(self, extra_users_args: dict | None = None):
        user_defaults = extra_users_args or {}

        if conf.MICROSOFT_SSO_UNIQUE_EMAIL:
            if not self.user_email:
                raise ValueError("User email not found in Tenant data.")
            if self.username_field.name not in user_defaults:
                user_defaults[self.username_field.name] = self.user_principal_name

            user, created = self.user_model.objects.get_or_create(
                email__iexact=self.user_email, defaults=user_defaults
            )
        else:
            user_defaults["email"] = self.user_email

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
                if "email" not in user_defaults:
                    user_defaults["email"] = self.user_email
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

        if conf.MICROSOFT_SSO_SAVE_BASIC_MICROSOFT_INFO:
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
        if created or conf.MICROSOFT_SSO_ALWAYS_UPDATE_USER_DATA:
            self.check_for_permissions(user)
            user.first_name = self.user_info.get("givenName") or ""
            user.last_name = self.user_info.get("surname") or ""
            user.email = self.user_email
            user.set_unusable_password()
            self.user_changed = True

    def check_first_super_user(self, user):
        if conf.MICROSOFT_SSO_AUTO_CREATE_FIRST_SUPERUSER:
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
        username = getattr(user, self.username_field.name, None)
        if (
            user.email in conf.MICROSOFT_SSO_STAFF_LIST
            or username in conf.MICROSOFT_SSO_STAFF_LIST
            or "*" in conf.MICROSOFT_SSO_STAFF_LIST
        ):
            message_text = _(
                f"User: {self.user_principal_name} in MICROSOFT_SSO_STAFF_LIST. "
                f"Added Staff Permission."
            )
            messages.add_message(self.request, messages.INFO, message_text)
            logger.debug(message_text)
            user.is_staff = True
        if (
            user.email in conf.MICROSOFT_SSO_SUPERUSER_LIST
            or username in conf.MICROSOFT_SSO_SUPERUSER_LIST
        ):
            message_text = _(
                f"User: {self.user_principal_name} in MICROSOFT_SSO_SUPERUSER_LIST. "
                f"Added SuperUser Permission."
            )
            messages.add_message(self.request, messages.INFO, message_text)
            logger.debug(message_text)
            user.is_superuser = True
            user.is_staff = True

    def find_user(self):
        if conf.MICROSOFT_SSO_UNIQUE_EMAIL:
            query = self.user_model.objects.filter(email__iexact=self.user_email)
        else:
            username_query = {
                f"{self.username_field.attname}__iexact": self.user_principal_name
            }
            query = self.user_model.objects.filter(
                Q(microsoftssouser__user_principal_name__iexact=self.user_principal_name)
                | Q(**username_query)
            )
        if query.exists():
            return query.get()
