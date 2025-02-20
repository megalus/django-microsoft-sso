# Using Django Admin

**Django Microsoft SSO** integrates with Django Admin, adding an Inline Model Admin to the User model. This way, you can
access the Microsoft SSO data for each user.

## Blocking password authentication

Setting `SSO_SHOW_FORM_ON_ADMIN_PAGE=False` doesn't block the default admin site's password login api. For that you
would need to override the default admin site's login method. Here is an example:

```python
from typing import Any

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.apps import AdminConfig
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed


class MyAdminSite(admin.AdminSite):
    ...
    
    def login(
        self, request: HttpRequest, extra_context: dict[str, Any] | None = None
    ) -> HttpResponse:
       if request.method != "GET" and not settings.SSO_SHOW_FORM_ON_ADMIN_PAGE:
            return HttpResponseNotAllowed(["GET"])
        return super().login(request, extra_context)


class MyAdminConfig(AdminConfig):
    default_site = "path.to.MyAdminSite"
```

See [Django docs](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#overriding-the-default-admin-site)
for more information on how to override the default admin site.


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
