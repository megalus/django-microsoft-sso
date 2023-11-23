# Using Django Admin

**Django Microsoft SSO** integrates with Django Admin, adding an Inline Model Admin to the User model. This way, you can
access the Microsoft SSO data for each user.

## Using Custom User model

If you are using a custom user model, you may need to add the `MicrosoftSSOInlineAdmin` inline model admin to your custom
user model admin, like this:

```python
# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django_microsoft_sso.admin import (
    MicrosoftSSOInlineAdmin, get_current_user_and_admin
)

CurrentUserModel, last_admin, LastUserAdmin = get_current_user_and_admin()

if admin.site.is_registered(CurrentUserModel):
    admin.site.unregister(CurrentUserModel)


@admin.register(CurrentUserModel)
class CustomUserAdmin(LastUserAdmin):
    inlines = (
        tuple(set(list(last_admin.inlines) + [MicrosoftSSOInlineAdmin]))
        if last_admin
        else (MicrosoftSSOInlineAdmin,)
    )
```

The `get_current_user_and_admin` helper function will return:

* the current registered **UserModel** in Django Admin (default: `django.contrib.auth.models.User`)
* the current registered **UserAdmin** in Django (default: `django.contrib.auth.admin.UserAdmin`)
* the **instance** of the current registered UserAdmin in Django (default: `None`)


Use this objects to maintain previous inlines and register your custom user model in Django Admin.
