from django.conf import settings
from loguru import logger

MICROSOFT_SSO_APPLICATION_ID = getattr(settings, "MICROSOFT_SSO_APPLICATION_ID", None)
MICROSOFT_SSO_CLIENT_SECRET = getattr(settings, "MICROSOFT_SSO_CLIENT_SECRET", None)
MICROSOFT_SSO_SCOPES = getattr(
    settings,
    "MICROSOFT_SSO_SCOPES",
    ["User.ReadBasic.All"],
)
MICROSOFT_SSO_TIMEOUT = getattr(settings, "MICROSOFT_SSO_TIMEOUT", 10)

MICROSOFT_SSO_ALLOWABLE_DOMAINS = getattr(settings, "MICROSOFT_SSO_ALLOWABLE_DOMAINS", [])
MICROSOFT_SSO_AUTO_CREATE_FIRST_SUPERUSER = getattr(
    settings, "MICROSOFT_SSO_AUTO_CREATE_FIRST_SUPERUSER", False
)
MICROSOFT_SSO_SESSION_COOKIE_AGE = getattr(
    settings, "MICROSOFT_SSO_SESSION_COOKIE_AGE", 3600
)
MICROSOFT_SSO_ENABLED = getattr(settings, "MICROSOFT_SSO_ENABLED", True)
MICROSOFT_SSO_SUPERUSER_LIST = getattr(settings, "MICROSOFT_SSO_SUPERUSER_LIST", [])
MICROSOFT_SSO_STAFF_LIST = getattr(settings, "MICROSOFT_SSO_STAFF_LIST", [])
MICROSOFT_SSO_CALLBACK_DOMAIN = getattr(settings, "MICROSOFT_SSO_CALLBACK_DOMAIN", None)
MICROSOFT_SSO_AUTO_CREATE_USERS = getattr(settings, "MICROSOFT_SSO_AUTO_CREATE_USERS", True)

MICROSOFT_SSO_AUTHENTICATION_BACKEND = getattr(
    settings, "MICROSOFT_SSO_AUTHENTICATION_BACKEND", None
)

MICROSOFT_SSO_PRE_VALIDATE_CALLBACK = getattr(
    settings,
    "MICROSOFT_SSO_PRE_VALIDATE_CALLBACK",
    "django_microsoft_sso.hooks.pre_validate_user",
)

MICROSOFT_SSO_PRE_CREATE_CALLBACK = getattr(
    settings,
    "MICROSOFT_SSO_PRE_CREATE_CALLBACK",
    "django_microsoft_sso.hooks.pre_create_user",
)

MICROSOFT_SSO_PRE_LOGIN_CALLBACK = getattr(
    settings,
    "MICROSOFT_SSO_PRE_LOGIN_CALLBACK",
    "django_microsoft_sso.hooks.pre_login_user",
)

MICROSOFT_SSO_LOGO_URL = getattr(
    settings,
    "MICROSOFT_SSO_LOGO_URL",
    "https://purepng.com/public/uploads/large/purepng.com-"
    "microsoft-logo-iconlogobrand-logoiconslogos-251519939091wmudn.png",
)

MICROSOFT_SSO_TEXT = getattr(settings, "MICROSOFT_SSO_TEXT", "Sign in with Microsoft")
MICROSOFT_SSO_NEXT_URL = getattr(settings, "MICROSOFT_SSO_NEXT_URL", "admin:index")
MICROSOFT_SSO_LOGIN_FAILED_URL = getattr(
    settings, "MICROSOFT_SSO_LOGIN_FAILED_URL", "admin:index"
)
MICROSOFT_SSO_SAVE_ACCESS_TOKEN = getattr(
    settings, "MICROSOFT_SSO_SAVE_ACCESS_TOKEN", False
)
MICROSOFT_SSO_ALWAYS_UPDATE_USER_DATA = getattr(
    settings, "MICROSOFT_SSO_ALWAYS_UPDATE_USER_DATA", False
)
MICROSOFT_SSO_LOGOUT_REDIRECT_PATH = getattr(
    settings, "MICROSOFT_SSO_LOGOUT_REDIRECT_PATH", "admin:index"
)
MICROSOFT_SLO_ENABLED = getattr(settings, "MICROSOFT_SLO_ENABLED", False)
SSO_USE_ALTERNATE_W003 = getattr(settings, "SSO_USE_ALTERNATE_W003", False)

if SSO_USE_ALTERNATE_W003:
    from django_microsoft_sso.checks.warnings import register_sso_check  # noqa

MICROSOFT_SSO_AUTHORITY = getattr(settings, "MICROSOFT_SSO_AUTHORITY", None)
MICROSOFT_SSO_UNIQUE_EMAIL = getattr(settings, "MICROSOFT_SSO_UNIQUE_EMAIL", False)
MICROSOFT_SSO_ENABLE_LOGS = getattr(settings, "MICROSOFT_SSO_ENABLE_LOGS", True)
MICROSOFT_SSO_ENABLE_MESSAGES = getattr(settings, "MICROSOFT_SSO_ENABLE_MESSAGES", True)
MICROSOFT_SSO_SAVE_BASIC_MICROSOFT_INFO = getattr(
    settings, "MICROSOFT_SSO_SAVE_BASIC_MICROSOFT_INFO", True
)
MICROSOFT_SSO_SHOW_FAILED_LOGIN_MESSAGE = getattr(
    settings, "MICROSOFT_SSO_SHOW_FAILED_LOGIN_MESSAGE", False
)


if MICROSOFT_SSO_ENABLE_LOGS:
    logger.enable("django_microsoft_sso")
else:
    logger.disable("django_microsoft_sso")
