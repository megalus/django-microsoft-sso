import httpx
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from loguru import logger


class MyBackend(ModelBackend):
    """Simple test for custom authentication backend"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        return super().authenticate(request, username, password, **kwargs)


def pre_login_callback(user, request):
    """Callback function called after user is logged in."""

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
        response = httpx.get(url, headers=headers)
        user_data = response.json()
        logger.debug(f"Updating User Data with Microsoft User Info: {user_data}")

        user.first_name = user_data["givenName"]
        user.last_name = user_data["surname"]
        user.email = user_data["mail"]
        user.save()
