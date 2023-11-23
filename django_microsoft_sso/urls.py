from django.urls import path

from django_microsoft_sso import conf, views

app_name = "django_microsoft_sso"

urlpatterns = []

if conf.MICROSOFT_SSO_ENABLED:
    urlpatterns += [
        path("login/", views.start_login, name="oauth_start_login"),
        path("callback/", views.callback, name="oauth_callback"),
    ]
