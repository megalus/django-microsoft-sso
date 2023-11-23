from django.http import HttpRequest

from django_microsoft_sso.models import User


def pre_login_user(user: User, request: HttpRequest) -> None:
    """
    Callback function called after user is created/retrieved but before logged in.
    """
