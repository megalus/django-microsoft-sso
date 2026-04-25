from tempfile import mkdtemp

from django.core.checks import run_checks


def _check_ids() -> list[str]:
    return [message.id for message in run_checks()]


def test_secure_callback_warns_for_non_shared_cache_backends(settings):
    # Arrange
    settings.CACHES = {
        "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}
    }
    settings.MICROSOFT_SSO_REQUIRE_SECURE_CALLBACK = True

    # Act
    check_ids = _check_ids()

    # Assert
    assert "sso.E001" not in check_ids
    assert "sso.W001" in check_ids


def test_secure_callback_accepts_shared_cache_backends_without_warning(settings):
    # Arrange
    settings.CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
            "LOCATION": mkdtemp(prefix="django_microsoft_sso_cache_"),
        }
    }
    settings.MICROSOFT_SSO_REQUIRE_SECURE_CALLBACK = True

    # Act
    check_ids = _check_ids()

    # Assert
    assert "sso.E001" not in check_ids
    assert "sso.W001" not in check_ids
