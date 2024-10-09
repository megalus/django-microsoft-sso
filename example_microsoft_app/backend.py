import arrow
import httpx
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from loguru import logger


class MyBackend(ModelBackend):
    """Simple test for custom authentication backend"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        return super().authenticate(request, username, password, **kwargs)


def pre_login_callback(user, request):
    """Callback function called before user is logged in."""

    # Example 1: Add SuperUser status to user
    messages.info(request, f"Running Pre-Login callback for user: {user}.")
    if not user.is_superuser or not user.is_staff:
        logger.info(f"Adding SuperUser status to email: {user.email}")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    # Example 2: Use Microsoft Info as a unique source of truth
    token = request.session.get("microsoft_sso_access_token")
    if token:
        headers = {
            "Authorization": f"Bearer {token}",
        }

        # Request Microsoft User Info
        # To retrieve user's additional data, you need to add the respective scope
        # For example: "User.Read.All" in settings MICROSOFT_SSO_SCOPES
        url = "https://graph.microsoft.com/v1.0/me/"
        response = httpx.get(url, headers=headers, timeout=10)
        user_data = response.json()
        logger.debug(f"Updating User Data with Microsoft User Info: {user_data}")

        user.first_name = user_data["givenName"]
        user.last_name = user_data["surname"]
        user.email = user_data["mail"]
        user.save()


def pre_create_callback(ms_info, request) -> dict:
    """Callback function called before user is created.

    return: dict content to be passed to User.objects.create() as `defaults` argument.
    """

    user_key = ms_info["mail"].split("@")[0]
    user_id = ms_info["id"].replace("-", "")

    username = f"{user_key}_{user_id}"

    url = "https://graph.microsoft.com/v1.0/organization"
    token = request.session.get("microsoft_sso_access_token")
    headers = {
        "Authorization": f"Bearer {token}",
    }
    response = httpx.get(url, timeout=10, headers=headers)
    response.raise_for_status()
    data = response.json()
    logger.debug(f"Organization Info: {data}")

    return {
        "username": username,
        "date_joined": arrow.utcnow().shift(days=-1).datetime,
    }


def pre_validate_callback(ms_info, request) -> bool:
    """Callback function called before user is validated.

    Must return a boolean to indicate if user is valid to login.

    params:
        ms_info: dict containing user info received from User Graph API.
        request: HttpRequest object.
    """
    messages.info(
        request, f"Running Pre-Validate callback for email: {ms_info.get('mail')}."
    )
    return True
