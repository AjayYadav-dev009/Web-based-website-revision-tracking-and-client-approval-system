from django.conf import settings


def test_django_settings_loaded():
    assert settings.SECRET_KEY
    assert "django.contrib.auth" in settings.INSTALLED_APPS
