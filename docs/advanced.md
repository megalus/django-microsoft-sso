# Advanced Use

## Using Custom Authentication Backend

If the users need to log in using a custom authentication backend, you can use the `MICROSOFT_SSO_AUTHENTICATION_BACKEND`
setting:

```python
# settings.py

MICROSOFT_SSO_AUTHENTICATION_BACKEND = "myapp.authentication.MyCustomAuthenticationBackend"
```

## Using Microsoft as Single Source of Truth

If you want to use Microsoft as the single source of truth for your users, you can simply set the
`MICROSOFT_SSO_ALWAYS_UPDATE_USER_DATA`. This will enforce the basic user data (first name, last name, email and picture) to be
updated at every login.

```python
# settings.py

MICROSOFT_SSO_ALWAYS_UPDATE_USER_DATA = True  # Always update user data on login
```

If you need more advanced logic, you can use the `MICROSOFT_SSO_PRE_LOGIN_CALLBACK` setting to import custom data from Microsoft
(considering you have configured the right scopes and possibly a Custom User model to store these fields).

For example, you can use the following code to update the user's
name, email and birthdate at every login:

```python
# settings.py

MICROSOFT_SSO_SAVE_ACCESS_TOKEN = True  # You will need this token
MICROSOFT_SSO_PRE_LOGIN_CALLBACK = "hooks.pre_login_user"
MICROSOFT_SSO_SCOPES = [
    "User.Read.All" # <-- custom scope to get all user basic data
]
```

```python
# myapp/hooks.py
import datetime
import httpx
from loguru import logger


def pre_login_user(user, request):
    token = request.session.get("microsoft_sso_access_token")
    if token:
        headers = {
            "Authorization": f"Bearer {token}",
        }

        # Request Microsoft User Info
        url = "https://graph.microsoft.com/v1.0/me/"
        response = httpx.get(url, headers=headers)
        user_data = response.json()
        logger.debug(f"Updating User Data with Microsoft User Info: {user_data}")

        user.first_name = user_data["givenName"]
        user.last_name = user_data["surname"]
        user.email = user_data["mail"]
        user.birthdate = user_data.get("birthday")  # You need a Custom User model to store this field
        user.save()
```
