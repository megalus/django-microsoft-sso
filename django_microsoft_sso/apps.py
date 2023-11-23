from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoMicrosoftSsoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_microsoft_sso"
    verbose_name = _("Microsoft SSO User")

    def ready(self):
        import django_microsoft_sso.templatetags  # noqa
