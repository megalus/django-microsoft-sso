# Setup Django URLs

The base configuration for Django URLs is the same we have described as before:
```python
# urls.py

from django.urls import include, path

urlpatterns = [
    # other urlpatterns...
    path(
        "microsoft_sso/", include(
            "django_microsoft_sso.urls",
            namespace="django_microsoft_sso"
        )
    ),
]
```
You can change the initial Path - `microsoft_sso/` - to whatever you want - just remember to change it on the
_Web Platform_ of your Registered Application as well.

## Overriding the Login view or Path

If you need to override the login view, or just the path, please add on the new view/class the
**Django SSO Admin** login template:

```python
from django.contrib.auth.views import LoginView
from django.urls import path


urlpatterns = [
    # other urlpatterns...
    path(
        "accounts/login/",
        LoginView.as_view(
            # The modified form with Microsoft button
            template_name="microsoft_sso/login.html"
        ),
    ),
]
```

or you can use a complete custom class:

```python
from django.contrib.auth.views import LoginView


class MyLoginView(LoginView):
    template_name = "microsoft_sso/login.html"
```
