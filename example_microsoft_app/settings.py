"""
Django settings for example_microsoft_app project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

from stela import env

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # Uncomment for Grappelli
    # "grappelli",
    # Uncomment for Jazzmin
    # "jazzmin",
    # Uncomment for Admin Interface
    # "admin_interface",
    # "colorfield",
    # Uncomment for Jest
    # "jet.dashboard",
    # "jet",
    # Uncomment for Unfold
    # "unfold",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",  # Need for Auth messages
    "django.contrib.staticfiles",
    "django.contrib.sites",  # Optional: Add Sites framework
    "django_microsoft_sso",  # Add django_microsoft_sso
    "django_google_sso",  # Optional: Add django_google_sso
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "example_microsoft_app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "NAME": "default",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "example_microsoft_app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

if "jet" in INSTALLED_APPS:
    # Jet Theme
    JET_DEFAULT_THEME = "light-gray"

    JET_THEMES = [
        {
            "theme": "default",  # theme folder name
            "color": "#47bac1",  # color of the theme's button in user menu
            "title": "Default",  # theme title
        },
        {"theme": "green", "color": "#44b78b", "title": "Green"},
        {"theme": "light-green", "color": "#2faa60", "title": "Light Green"},
        {"theme": "light-violet", "color": "#a464c4", "title": "Light Violet"},
        {"theme": "light-blue", "color": "#5EADDE", "title": "Light Blue"},
        {"theme": "light-gray", "color": "#222", "title": "Light Gray"},
    ]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "example_microsoft_app" / "static"]


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = ["example_microsoft_app.backend.MyBackend"]


SITE_ID = 1

###############################
#                             #
# Test Microsoft              #
#                             #
###############################

# Uncomment MICROSOFT_SSO_CALLBACK_DOMAIN to use Sites Framework site domain
# Or comment both and use domain retrieved from accounts/login/ request
MICROSOFT_SSO_CALLBACK_DOMAIN = env.MICROSOFT_SSO_CALLBACK_DOMAIN

MICROSOFT_SSO_APPLICATION_ID = env.MICROSOFT_SSO_APPLICATION_ID
MICROSOFT_SSO_CLIENT_SECRET = env.MICROSOFT_SSO_CLIENT_SECRET

MICROSOFT_SSO_ALLOWABLE_DOMAINS = env.get_or_default("MICROSOFT_SSO_ALLOWABLE_DOMAINS", [])
MICROSOFT_SSO_AUTO_CREATE_FIRST_SUPERUSER = (
    False  # Mark as True, to create superuser on first eligible user login
)
MICROSOFT_SSO_STAFF_LIST = env.get_or_default("MICROSOFT_SSO_STAFF_LIST", [])

MICROSOFT_SSO_SUPERUSER_LIST = env.get_or_default("MICROSOFT_SSO_SUPERUSER_LIST", [])

# Optional: You can save access token to session
MICROSOFT_SSO_SAVE_ACCESS_TOKEN = True

# Optional: Start or Stop User auto-creation
# MICROSOFT_SSO_AUTO_CREATE_USERS = True

# Optional: Show failed login attempt message on browser.
# This message can be used in exploit attempts.
# MICROSOFT_SSO_SHOW_FAILED_LOGIN_MESSAGE = False

# Optional: Add if you want to use custom authentication backend
# MICROSOFT_SSO_AUTHENTICATION_BACKEND = "backend.MyBackend"

# Optional: Change Scopes
MICROSOFT_SSO_SCOPES = [
    # "User.ReadBasic.All"  # default scope
    "User.Read.All",  # additional scope
]

# Optional: Add pre-validate logic
MICROSOFT_SSO_PRE_VALIDATE_CALLBACK = "backend.pre_validate_callback"

# Optional: Add pre-create logic
MICROSOFT_SSO_PRE_CREATE_CALLBACK = "backend.pre_create_callback"

# Optional: Add pre-login logic
# MICROSOFT_SSO_PRE_LOGIN_CALLBACK = "backend.pre_login_callback"

# Optional: Always update user data
MICROSOFT_SSO_ALWAYS_UPDATE_USER_DATA = True

# Optional: Customize Button Text
# MICROSOFT_SSO_TEXT = "Login using Microsoft 365 Account"

# Optional: Disable Logs
# MICROSOFT_SSO_ENABLE_LOGS = False

# Optional: Disable Django Messages
# MICROSOFT_SSO_ENABLE_MESSAGES = False

###############################
#                             #
# Test Google                 #
#                             #
###############################

# Uncomment GOOGLE_SSO_CALLBACK_DOMAIN to use Sites Framework site domain
# Or comment both and use domain retrieved from accounts/login/ request
GOOGLE_SSO_CALLBACK_DOMAIN = env.GOOGLE_SSO_CALLBACK_DOMAIN

GOOGLE_SSO_SESSION_COOKIE_AGE = 3600  # default value
GOOGLE_SSO_CLIENT_ID = env.GOOGLE_SSO_CLIENT_ID
GOOGLE_SSO_PROJECT_ID = env.GOOGLE_SSO_PROJECT_ID
GOOGLE_SSO_CLIENT_SECRET = env.GOOGLE_SSO_CLIENT_SECRET

GOOGLE_SSO_ALLOWABLE_DOMAINS = env.get_or_default("GOOGLE_SSO_ALLOWABLE_DOMAINS", [])
GOOGLE_SSO_AUTO_CREATE_FIRST_SUPERUSER = (
    False  # Mark as True, to create superuser on first eligible user login
)
GOOGLE_SSO_STAFF_LIST = env.get_or_default("GOOGLE_SSO_STAFF_LIST", [])
GOOGLE_SSO_SUPERUSER_LIST = env.get_or_default("GOOGLE_SSO_SUPERUSER_LIST", [])
GOOGLE_SSO_TIMEOUT = 10  # default value
GOOGLE_SSO_SCOPES = [  # default values
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    # "https://www.googleapis.com/auth/user.birthday.read",  # additional scope
]

# Optional: Add if you want to use custom authentication backend
GOOGLE_SSO_AUTHENTICATION_BACKEND = "backend.MyBackend"

# Optional: You can save access token to session
# GOOGLE_SSO_SAVE_ACCESS_TOKEN = True

# Optional: Add pre-login logic
# GOOGLE_SSO_PRE_LOGIN_CALLBACK = "backend.pre_login_callback"

# Uncomment to disable SSO login
# GOOGLE_SSO_ENABLED = False  # default: True

GOOGLE_SSO_LOGO_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/"
    "Google_%22G%22_logo.svg/1280px-Google_%22G%22_logo.svg.png"
)

# Uncomment to disable user auto-creation
# GOOGLE_SSO_AUTO_CREATE_USERS = False  # default: True

# Uncomment to hide login form on admin page
# SSO_SHOW_FORM_ON_ADMIN_PAGE = False  # default: True

# If you're using more than one SSO provider,
# you can full disable django's E003/W003 check, uncomment the
# SILENCED_SYSTEM_CHECKS option
# To use an alternate version for this check,
# which filters SSO templates, uncomment both options:
SILENCED_SYSTEM_CHECKS = ["templates.W003"]
SSO_USE_ALTERNATE_W003 = True  # default: False
