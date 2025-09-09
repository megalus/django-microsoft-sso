from typing import Any, Callable

from django.conf import settings
from django.http import HttpRequest
from loguru import logger


class MicrosoftSSOSettings:
    """
    Settings class for Microsoft SSO.

    This class implements properties for all Microsoft SSO settings.
    Some settings accept callable values that will be called with the current request.
    """

    def _get_setting(
        self, name: str, default: Any = None, accept_callable: bool = True
    ) -> Any:
        """Get a setting from Django settings."""
        value = getattr(settings, name, default)
        if not accept_callable and callable(value):
            raise TypeError(f"The setting {name} cannot be a callable.")
        return value

    # Configurations without callable
    @property
    def MICROSOFT_SSO_ENABLED(self) -> bool:
        return self._get_setting("MICROSOFT_SSO_ENABLED", True, accept_callable=False)

    @property
    def MICROSOFT_SSO_ENABLE_LOGS(self) -> bool:
        value = self._get_setting("MICROSOFT_SSO_ENABLE_LOGS", True, accept_callable=False)
        if value:
            logger.enable("django_microsoft_sso")
        else:
            logger.disable("django_microsoft_sso")
        return value

    @property
    def SSO_USE_ALTERNATE_W003(self) -> bool:
        return self._get_setting("SSO_USE_ALTERNATE_W003", False, accept_callable=False)

    # Configurations with optional callable

    @property
    def MICROSOFT_SSO_LOGO_URL(self) -> str | Callable[[HttpRequest], str]:
        return self._get_setting(
            "MICROSOFT_SSO_LOGO_URL",
            "https://purepng.com/public/uploads/large/purepng.com-"
            "microsoft-logo-iconlogobrand-logoiconslogos-251519939091wmudn.png",
        )

    @property
    def MICROSOFT_SSO_TEXT(self) -> str | Callable[[HttpRequest], str]:
        return self._get_setting("MICROSOFT_SSO_TEXT", "Sign in with Microsoft")

    @property
    def MICROSOFT_SSO_ADMIN_ENABLED(self) -> bool | Callable[[HttpRequest], str] | None:
        return self._get_setting("MICROSOFT_SSO_ADMIN_ENABLED", None)

    @property
    def MICROSOFT_SSO_PAGES_ENABLED(self) -> bool | Callable[[HttpRequest], str] | None:
        return self._get_setting("MICROSOFT_SSO_PAGES_ENABLED", None)

    @property
    def MICROSOFT_SSO_APPLICATION_ID(self) -> str | Callable[[HttpRequest], str] | None:
        return self._get_setting("MICROSOFT_SSO_APPLICATION_ID", None)

    @property
    def MICROSOFT_SSO_CLIENT_SECRET(self) -> str | Callable[[HttpRequest], str] | None:
        return self._get_setting("MICROSOFT_SSO_CLIENT_SECRET", None)

    @property
    def MICROSOFT_SSO_SCOPES(self) -> list[str] | Callable[[HttpRequest], list[str]]:
        return self._get_setting("MICROSOFT_SSO_SCOPES", ["User.ReadBasic.All"])

    @property
    def MICROSOFT_SSO_TIMEOUT(self) -> int | Callable[[HttpRequest], int]:
        return self._get_setting("MICROSOFT_SSO_TIMEOUT", 10)

    @property
    def MICROSOFT_SSO_ALLOWABLE_DOMAINS(
        self,
    ) -> list[str] | Callable[[HttpRequest], list[str]]:
        return self._get_setting("MICROSOFT_SSO_ALLOWABLE_DOMAINS", [])

    @property
    def MICROSOFT_SSO_AUTO_CREATE_FIRST_SUPERUSER(
        self,
    ) -> bool | Callable[[HttpRequest], bool]:
        return self._get_setting("MICROSOFT_SSO_AUTO_CREATE_FIRST_SUPERUSER", False)

    @property
    def MICROSOFT_SSO_SESSION_COOKIE_AGE(self) -> int | Callable[[HttpRequest], int]:
        return self._get_setting("MICROSOFT_SSO_SESSION_COOKIE_AGE", 3600)

    @property
    def MICROSOFT_SSO_SUPERUSER_LIST(
        self,
    ) -> list[str] | Callable[[HttpRequest], list[str]]:
        return self._get_setting("MICROSOFT_SSO_SUPERUSER_LIST", [])

    @property
    def MICROSOFT_SSO_STAFF_LIST(self) -> list[str] | Callable[[HttpRequest], list[str]]:
        return self._get_setting("MICROSOFT_SSO_STAFF_LIST", [])

    @property
    def MICROSOFT_SSO_CALLBACK_DOMAIN(self) -> str | Callable[[HttpRequest], str] | None:
        return self._get_setting("MICROSOFT_SSO_CALLBACK_DOMAIN", None)

    @property
    def MICROSOFT_SSO_AUTO_CREATE_USERS(self) -> bool | Callable[[HttpRequest], bool]:
        return self._get_setting("MICROSOFT_SSO_AUTO_CREATE_USERS", True)

    @property
    def MICROSOFT_SSO_AUTHENTICATION_BACKEND(
        self,
    ) -> str | Callable[[HttpRequest], str] | None:
        return self._get_setting("MICROSOFT_SSO_AUTHENTICATION_BACKEND", None)

    @property
    def MICROSOFT_SSO_PRE_VALIDATE_CALLBACK(self) -> str | Callable[[HttpRequest], str]:
        return self._get_setting(
            "MICROSOFT_SSO_PRE_VALIDATE_CALLBACK",
            "django_microsoft_sso.hooks.pre_validate_user",
        )

    @property
    def MICROSOFT_SSO_PRE_CREATE_CALLBACK(self) -> str | Callable[[HttpRequest], str]:
        return self._get_setting(
            "MICROSOFT_SSO_PRE_CREATE_CALLBACK",
            "django_microsoft_sso.hooks.pre_create_user",
        )

    @property
    def MICROSOFT_SSO_PRE_LOGIN_CALLBACK(self) -> str | Callable[[HttpRequest], str]:
        return self._get_setting(
            "MICROSOFT_SSO_PRE_LOGIN_CALLBACK",
            "django_microsoft_sso.hooks.pre_login_user",
        )

    @property
    def MICROSOFT_SSO_NEXT_URL(self) -> str | Callable[[HttpRequest], str]:
        return self._get_setting("MICROSOFT_SSO_NEXT_URL", "admin:index")

    @property
    def MICROSOFT_SSO_LOGIN_FAILED_URL(self) -> str | Callable[[HttpRequest], str]:
        return self._get_setting("MICROSOFT_SSO_LOGIN_FAILED_URL", "admin:login")

    @property
    def MICROSOFT_SSO_SAVE_ACCESS_TOKEN(self) -> bool | Callable[[HttpRequest], bool]:
        return self._get_setting("MICROSOFT_SSO_SAVE_ACCESS_TOKEN", False)

    @property
    def MICROSOFT_SSO_ALWAYS_UPDATE_USER_DATA(self) -> bool | Callable[[HttpRequest], bool]:
        return self._get_setting("MICROSOFT_SSO_ALWAYS_UPDATE_USER_DATA", False)

    @property
    def MICROSOFT_SSO_LOGOUT_REDIRECT_PATH(self) -> str | Callable[[HttpRequest], str]:
        return self._get_setting("MICROSOFT_SSO_LOGOUT_REDIRECT_PATH", "admin:index")

    @property
    def MICROSOFT_SLO_ENABLED(self) -> bool | Callable[[HttpRequest], bool]:
        return self._get_setting("MICROSOFT_SLO_ENABLED", False)

    @property
    def MICROSOFT_SSO_AUTHORITY(self) -> Any | Callable[[HttpRequest], Any]:
        return self._get_setting("MICROSOFT_SSO_AUTHORITY", None)

    @property
    def MICROSOFT_SSO_UNIQUE_EMAIL(self) -> bool | Callable[[HttpRequest], bool]:
        return self._get_setting("MICROSOFT_SSO_UNIQUE_EMAIL", False)

    @property
    def MICROSOFT_SSO_ENABLE_MESSAGES(self) -> bool | Callable[[HttpRequest], bool]:
        return self._get_setting("MICROSOFT_SSO_ENABLE_MESSAGES", True)

    @property
    def MICROSOFT_SSO_SAVE_BASIC_MICROSOFT_INFO(
        self,
    ) -> bool | Callable[[HttpRequest], bool]:
        return self._get_setting("MICROSOFT_SSO_SAVE_BASIC_MICROSOFT_INFO", True)

    @property
    def MICROSOFT_SSO_SHOW_FAILED_LOGIN_MESSAGE(
        self,
    ) -> bool | Callable[[HttpRequest], bool]:
        return self._get_setting("MICROSOFT_SSO_SHOW_FAILED_LOGIN_MESSAGE", False)

    @property
    def MICROSOFT_SSO_SLO_ENABLED(
        self,
    ) -> bool | Callable[[HttpRequest], bool]:
        return self._get_setting("MICROSOFT_SSO_SLO_ENABLED", False)

    @property
    def MICROSOFT_SSO_GRAPH_TIMEOUT(self) -> int | Callable[[HttpRequest], int]:
        return self._get_setting("MICROSOFT_SSO_GRAPH_TIMEOUT", 10)

    @property
    def SSO_ADMIN_ROUTE(
        self,
    ) -> str | Callable[[HttpRequest], str]:
        return self._get_setting("SSO_ADMIN_ROUTE", "admin:index")

    @property
    def SSO_SHOW_FORM_ON_ADMIN_PAGE(
        self,
    ) -> bool | Callable[[HttpRequest], bool]:
        return self._get_setting("SSO_SHOW_FORM_ON_ADMIN_PAGE", True)


# Create a single instance of the settings class
_ms_sso_settings = MicrosoftSSOSettings()


def __getattr__(name: str) -> Any:
    """
    Implement PEP 562 __getattr__ to lazily load settings.

    This function is called when an attribute is not found in the module's
    global namespace. It delegates to the _ms_sso_settings instance.
    """
    return getattr(_ms_sso_settings, name)


if _ms_sso_settings.SSO_USE_ALTERNATE_W003:
    from django_microsoft_sso.checks.warnings import register_sso_check  # noqa

if _ms_sso_settings.MICROSOFT_SSO_ENABLE_LOGS:
    logger.enable("django_microsoft_sso")
else:
    logger.disable("django_microsoft_sso")
