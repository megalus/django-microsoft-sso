<p align="center">
  <img src="docs/images/django-microsoft-sso.png" alt="Django Microsoft SSO"/>
</p>
<p align="center">
<em>Easily integrate Microsoft Authentication into your Django projects</em>
</p>

<p align="center">
<a href="https://pypi.org/project/django-microsoft-sso/" target="_blank">
<img alt="PyPI" src="https://img.shields.io/pypi/v/django-microsoft-sso"/></a>
<a href="https://github.com/megalus/django-microsoft-sso/actions" target="_blank">
<img alt="Build" src="https://github.com/megalus/django-microsoft-sso/workflows/tests/badge.svg"/>
</a>
<a href="https://www.python.org" target="_blank">
<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/django-microsoft-sso"/>
</a>
<a href="https://www.djangoproject.com/" target="_blank">
<img alt="PyPI - Django Version" src="https://img.shields.io/pypi/djversions/django-microsoft-sso"/>
</a>
</p>

## Welcome to Django Microsoft SSO

This library aims to simplify the process of authenticating users with Microsoft in Django Admin pages,
inspired by libraries like [django_microsoft_auth](https://github.com/AngellusMortis/django_microsoft_auth)
and [django-admin-sso](https://github.com/matthiask/django-admin-sso/)

---

### Documentation

* Docs: https://megalus.github.io/django-microsoft-sso/

---

### Install

```shell
$ pip install django-microsoft-sso
```

### Configure

1. Add the following to your `settings.py` `INSTALLED_APPS`:

```python
# settings.py

INSTALLED_APPS = [
    # other django apps
    "django.contrib.messages",  # Need for Auth messages
    "django_microsoft_sso",  # Add django_microsoft_sso
]
```

2. In [Microsoft Entra Administration Center](https://entra.microsoft.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade/quickStartType~/null/sourceType/Microsoft_AAD_IAM) at _Application Register_, retrieve your
   Application ID. Navigate to **Certificate & secrets** link, and get the **Client Secret Value**. Add both in your `settings.py`:

```python
# settings.py

MICROSOFT_SSO_APPLICATION_ID = "your Application ID here"
MICROSOFT_SSO_CLIENT_SECRET = "your Client Secret Value here"
```

3. Add the callback uri `http://localhost:8000/microsoft_sso/callback/` in your Microsoft Console, on the "Authorized Redirect
   URL".

4. Let Django Microsoft SSO auto create users for allowable domains:

```python
# settings.py

MICROSOFT_SSO_ALLOWABLE_DOMAINS = ["contoso.com"]
```

5. In `urls.py` please add the **Django-Microsoft-SSO** views:

```python
# urls.py

from django.urls import include, path

urlpatterns = [
    # other urlpatterns...
    path(
        "microsoft_sso/", include("django_microsoft_sso.urls", namespace="django_microsoft_sso")
    ),
]
```

6. And run migrations:

```shell
$ python manage.py migrate
```

That's it. Start django on port 8000 and open your browser in `http://localhost:8000/admin/login` and you should see the
Microsoft SSO button.

<p align="center">
   <img src="docs/images/django_login_with_microsoft_light.png"/>
</p>

---

## License

This project is licensed under the terms of the MIT license.
