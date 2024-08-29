# Auto Creating Users

**Django Microsoft SSO** can automatically create users from Microsoft SSO authentication. To enable this feature, you need to
set the `MICROSOFT_SSO_ALLOWABLE_DOMAINS` setting in your `settings.py`, with a list of domains that will be allowed to create.
For example, if any user with a gmail account can sign in, you can set:

```python
# settings.py
MICROSOFT_SSO_ALLOWABLE_DOMAINS = ["contoso.com"]
```

## Disabling the auto-create users

You can disable the auto-create users feature by setting the `MICROSOFT_SSO_AUTO_CREATE_USERS` setting to `False`:

```python
MICROSOFT_SSO_AUTO_CREATE_USERS = False
```

You can also disable the plugin completely:

```python
MICROSOFT_SSO_ENABLED = False
```

## Giving Permissions to Auto-Created Users

If you are using the auto-create users feature, you can give permissions to the users that are created automatically. To do
this, you can set the following options in your `settings.py`:

```python
# List of emails or user principal names that will be created as staff
MICROSOFT_SSO_STAFF_LIST = ["my-email@contoso.com"]

# List of emails or user principal names that will be created as superuser
MICROSOFT_SSO_SUPERUSER_LIST = ["another-email@contoso.com"]

# If True, the first user that checks in will be created as superuser
# if no superuser exists in the database at all
MICROSOFT_SSO_AUTO_CREATE_FIRST_SUPERUSER = True
```

For staff user creation _only_, you can add all users using "*" as the value:

```python
# Use "*" to add all users as staff
MICROSOFT_SSO_STAFF_LIST = ["*"]
```

## Fine-tuning validation before user validation

If you need to do some custom validation _before_ user is validated, you can set the
`MICROSOFT_SSO_PRE_VALIDATE_CALLBACK` setting to import a custom function that will be called before the user is created.
This function will receive two arguments: the `ms_gragh_info` dict from User Graph API response and `request` objects.

```python
# myapp/hooks.py
def pre_validate_user(ms_graph_info, request):
    # Check some info from ms_graph_info and/or request
    return True  # The user can be created
```

Please note, even if this function returns `True`, the user can be denied if their email is not valid.


## Fine-tuning user info before user creation

If you need to do some processing _before_ user is created, you can set the
`MICROSOFT_SSO_PRE_CREATE_CALLBACK` setting to import a custom function that will be called before the user is created.
This function will receive two arguments: the `ms_user_info` dict from Graph User API and `request` objects.

!!! tip "You can add custom fields to the user model here"

    The `pre_create_callback` function can return a dictionary with the fields and values that will be passed to
    `User.objects.create()` as the `defaults` argument. This means you can add custom fields to the user model here or
    change default values for some fields, like `username`.

    If not defined, the field `username` is always the User Principal Name.

    You can't change the fields: `first_name`, `last_name`, `email` and `password` using this callback. These fields are
    always passed to `User.objects.create()` with the values from Graph API and the password is always unusable.


```python
import arrow

def pre_create_callback(ms_info, request) -> dict | None:
    """Callback function called before user is created.

    return: dict content to be passed to
            User.objects.create() as `defaults` argument.
            If not informed, field `username` is always
            the user principal name.
    """

    user_key = ms_info["mail"].split("@")[0]
    user_id = ms_info["id"].replace("-", "")

    username = f"{user_key}_{user_id}"

    return {
        "username": username,
        "date_joined": arrow.utcnow().shift(days=-1).datetime,
    }
```

## Fine-tuning users before login

If you need to do some processing _after_ user is created or retrieved,
but _before_ the user is logged in, you can set the
`MICROSOFT_SSO_PRE_LOGIN_CALLBACK` setting to import a custom function that will be called before the user is logged in.
This function will receive two arguments: the `user` and `request` objects.

```python
# myapp/hooks.py
def pre_login_user(user, request):
    # Do something with the user
    pass

# settings.py
MICROSOFT_SSO_PRE_LOGIN_CALLBACK = "myapp.hooks.pre_login_user"
```

Please remember this function will be invoked only if a user exists, and if it is active.
In other words, if the user is eligible for login.

!!! tip "You can add your hooks to customize all steps:"
    * `MICROSOFT_SSO_PRE_VALIDATE_CALLBACK`: Run before the user is validated.
    * `MICROSOFT_SSO_PRE_CREATE_CALLBACK`: Run before the user is created.
    * `MICROSOFT_SSO_PRE_LOGIN_CALLBACK`: Run before the user is logged in.


!!! warning "Be careful with these options"
    The idea here is to make your life easier, especially when testing. But if you are not careful, you can give
    permissions to users that you don't want, or even worse, you can give permissions to users that you don't know.
    So, please, be careful with these options.

---

For the last step, we will look at the Django URLs.
