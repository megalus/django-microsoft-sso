# Getting Microsoft info

## The User model

**Django Microsoft SSO** saves in the database the following information from Microsoft, using current `User` model:

* `email`: The email address of the user.
* `first_name`: The first name of the user.
* `last_name`: The last name of the user.
* `username`: The email address of the user.
* `password`: An unusable password, generated using `get_unusable_password()` from Django.

Getting data on code is straightforward:

```python
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest

@login_required
def retrieve_user_data(request: HttpRequest) -> JsonResponse:
    user = request.user
    return JsonResponse({
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
    })
```

## The MicrosoftSSOUser model

Also, on the `MicrosoftSSOUser` model, it saves the following information:

* `picture_raw`: The binary data of the user's profile picture.
* `microsoft_id`: The Microsoft Entra ID of the user.
* `locale`: The preferred locale of the user.

This is a one-to-one relationship with the `User` model, so you can access this data using the `microsoftssouser` reverse
relation attribute:

```python
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest

@login_required
def retrieve_user_data(request: HttpRequest) -> JsonResponse:
    user = request.user
    return JsonResponse({
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "picture": user.microsoftssouser.picture_raw,
        "microsoft_id": user.microsoftssouser.microsoft_id,
        "locale": user.microsoftssouser.locale,
    })
```

You can also import the model directly, like this:

```python
from django_microsoft_sso.models import MicrosoftSSOUser

microsoft_info = MicrosoftSSOUser.objects.get(user=user)
```

## About Microsoft Scopes

To retrieve this data, **Django Microsoft SSO** uses the following scope from [Microsoft Graph reference](https://learn.microsoft.com/en-us/graph/permissions-reference):

```python
MICROSOFT_SSO_SCOPES = [  # Microsoft default scope
    "User.ReadBasic.All"
]
```

You can change this scopes overriding the `MICROSOFT_SSO_SCOPES` setting in your `settings.py` file. But if you ask the user
to authorize more scopes, this plugin will not save this additional data in the database. You will need to implement
your own logic to save this data, calling Microsoft again. You can see an example [here](./how.md).

!!! info "The main goal here is simplicity"
    The main goal of this plugin is to be simple to use as possible. But it is important to ask the user **_once_** for the scopes.
    That's why this plugin permits you to change the scopes, but will not save the additional data from it.

## The Access Token
To make login possible, **Django Microsoft SSO** needs to get an access token from Microsoft. This token is used to retrieve
User info to get or create the user in the database. If you need this access token, you can get it inside the User Request
Session, like this:

```python
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest

@login_required
def retrieve_user_data(request: HttpRequest) -> JsonResponse:
    user = request.user
    return JsonResponse({
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "picture": user.microsoftssouser.picture_raw,
        "microsoft_id": user.microsoftssouser.microsoft_id,
        "locale": user.microsoftssouser.locale,
        "access_token": request.session["microsoft_sso_access_token"],
    })
```

Saving the Access Token in User Session is disabled, by default, to avoid security issues. If you need to enable it,
you can set the configuration `MICROSOFT_SSO_SAVE_ACCESS_TOKEN` to `True` in your `settings.py` file. Please make sure you
understand how to [secure your cookies](https://docs.djangoproject.com/en/4.2/ref/settings/#session-cookie-secure)
before enabling this option.

## The Access Token
To make login possible, **Django Google SSO** needs to get an access token from Google. This token is used to retrieve
User info to get or create the user in the database. If you need this access token, you can get it inside the User Request
Session, like this:

```python
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest

@login_required
def retrieve_user_data(request: HttpRequest) -> JsonResponse:
    user = request.user
    return JsonResponse({
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "picture": user.googlessouser.picture_url,
        "google_id": user.googlessouser.google_id,
        "locale": user.googlessouser.locale,
        "access_token": request.session["google_sso_access_token"],
    })
```

Saving the Access Token in User Session is disabled, by default, to avoid security issues. If you need to enable it,
you can set the configuration `GOOGLE_SSO_SAVE_ACCESS_TOKEN` to `True` in your `settings.py` file. Please make sure you
understand how to [secure your cookies](https://docs.djangoproject.com/en/4.2/ref/settings/#session-cookie-secure)
before enabling this option.
