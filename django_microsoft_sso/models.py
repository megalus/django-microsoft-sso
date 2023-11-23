from base64 import b64encode

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class MicrosoftSSOUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    microsoft_id = models.CharField(max_length=255, blank=True, null=True)
    picture_raw = models.BinaryField(blank=True, null=True)
    locale = models.CharField(max_length=5, blank=True, null=True)

    @property
    def picture(self):
        if self.picture_raw:
            return mark_safe(
                '<img src = "data: image/png; base64, {}"'
                ' width="75" height="75">'.format(
                    b64encode(self.picture_raw).decode("utf8")
                )
            )
        return None

    def __str__(self):
        return f"{self.user.email} ({self.microsoft_id})"

    class Meta:
        db_table = "microsoft_sso_user"
        verbose_name = _("Microsoft SSO User")
