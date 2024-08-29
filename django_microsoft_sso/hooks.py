from django.http import HttpRequest

from django_microsoft_sso.models import User


def pre_login_user(user: User, request: HttpRequest) -> None:
    """
    Callback function called after user is created/retrieved but before logged in.
    """


def pre_create_user(ms_user_info: dict, request: HttpRequest) -> dict | None:
    """
    Callback function called before user is created.

    params:
        ms_user_info: dict containing user info received from Microsoft Graph.
        request: HttpRequest object.

    return: dict content to be passed to User.objects.create() as `defaults` argument.
    """
    return {}


def pre_validate_user(ms_user_info: dict, request: HttpRequest) -> bool:
    """
    Callback function called before user is validated.

    Must return a boolean to indicate if user is valid to login.

    params:
        ms_user_info: dict containing user info received from Microsoft Graph.
        request: HttpRequest object.
    """
    return True
