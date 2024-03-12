import uuid
from dataclasses import dataclass
from typing import Any

import httpx
import msal
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from loguru import logger
from msal import ConfidentialClientApplication

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
            self._auth = msal.ConfidentialClientApplication(
                client_id=conf.MICROSOFT_SSO_APPLICATION_ID,
                client_credential=conf.MICROSOFT_SSO_CLIENT_SECRET,
            )
        return self._auth

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
    def user_email(self):
        return self.user_info["mail"]

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

    def get_or_create_user(self):
        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            email=self.user_email, defaults={"username": self.user_email}
        )
        self.check_first_super_user(user, user_model)
        self.check_for_update(created, user)
        if self.user_changed:
            user.save()

        MicrosoftSSOUser.objects.update_or_create(
            user=user,
            defaults={
                "microsoft_id": self.user_info["id"],
                "picture_raw": self.user_info["picture_raw_data"],
                "locale": self.user_info["preferredLanguage"],
            },
        )

        return user

    def check_for_update(self, created, user):
        if created or conf.MICROSOFT_SSO_ALWAYS_UPDATE_USER_DATA:
            self.check_for_permissions(user)
            user.first_name = self.user_info["givenName"]
            user.last_name = self.user_info["surname"]
            user.username = self.user_info["userPrincipalName"]
            user.set_unusable_password()
            self.user_changed = True

    def check_first_super_user(self, user, user_model):
        if conf.MICROSOFT_SSO_AUTO_CREATE_FIRST_SUPERUSER:
            superuser_exists = user_model.objects.filter(
                is_superuser=True, email__contains=f"@{self.user_email.split('@')[-1]}"
            ).exists()
            if not superuser_exists:
                message_text = _(
                    f"MICROSOFT_SSO_AUTO_CREATE_FIRST_SUPERUSER is True. "
                    f"Adding SuperUser status to email: {self.user_email}"
                )
                messages.add_message(self.request, messages.INFO, message_text)
                logger.warning(message_text)
                user.is_superuser = True
                user.is_staff = True
                self.user_changed = True

    def check_for_permissions(self, user):
        if user.email in conf.MICROSOFT_SSO_STAFF_LIST:
            message_text = _(
                f"User email: {self.user_email} in MICROSOFT_SSO_STAFF_LIST. "
                f"Added Staff Permission."
            )
            messages.add_message(self.request, messages.INFO, message_text)
            logger.debug(message_text)
            user.is_staff = True
        if user.email in conf.MICROSOFT_SSO_SUPERUSER_LIST:
            message_text = _(
                f"User email: {self.user_email} in MICROSOFT_SSO_SUPERUSER_LIST. "
                f"Added SuperUser Permission."
            )
            messages.add_message(self.request, messages.INFO, message_text)
            logger.debug(message_text)
            user.is_superuser = True
            user.is_staff = True

    def find_user(self):
        user_model = get_user_model()
        query = user_model.objects.filter(email=self.user_email)
        if query.exists():
            return query.get()
