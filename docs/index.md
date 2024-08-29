![](images/django-microsoft-sso.png)

# Welcome to Django Microsoft SSO

## Motivation

This library aims to simplify the process of authenticating users with Microsoft in Django Admin pages,
inspired by libraries like [django_microsoft_auth](https://github.com/AngellusMortis/django_microsoft_auth)
and [django-admin-sso](https://github.com/matthiask/django-admin-sso/)

## Why another library?

* This library aims for _simplicity_ and ease of use. [django-allauth](https://github.com/pennersr/django-allauth) is
  _de facto_ solution for Authentication in Django, but add lots of boilerplate, specially the html templates.
  **Django-Microsoft-SSO** just add the "Login with Google" button in the default login page.

    === "Light Mode"
        ![](images/django_login_with_microsoft_light.png)

    === "Dark Mode"
        ![](images/django_login_with_microsoft_dark.png)

* [django_microsoft_auth](https://github.com/AngellusMortis/django_microsoft_auth) is a bit outated but you can use it for old python and
  django versions.
* Microsoft provides a complete tutorial
  here: https://learn.microsoft.com/en-us/training/modules/msid-django-web-app-sign-in/, with very good insights,
  but it's a bit outdated and doesn't provide the social button.

---

## Install

```shell
pip install django-microsoft-sso
```

!!! info "Currently this project supports:"
    * Python 3.10, 3.11 and 3.12
    * Django 4.2, 5.0 and 5.1
