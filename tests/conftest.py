from __future__ import annotations

from pathlib import Path

import pytest
from django.conf import settings
from django.test.utils import override_settings

TEST_SETTINGS = {
    "DEBUG": False,
    "SECRET_KEY": "testing",
    "DATABASES": {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        },
    },
    "TEMPLATES": [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [
                Path(settings.BASE_DIR, "templates"),
            ],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
                "debug": True,
            },
        }
    ],
    "PASSWORD_HASHERS": [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ],
    "WHITENOISE_AUTOREFRESH": True,
    "STORAGES": {
        "default": {
            "BACKEND": "django.core.files.storage.InMemoryStorage",
        },
        "staticfiles": {
            "BACKEND": "django.core.files.storage.InMemoryStorage",
        },
    },
    "AUTHENTICATION_BACKENDS": [
        "django.contrib.auth.backends.ModelBackend",
    ],
    "EMAIL_BACKEND": "django.core.mail.backends.locmem.EmailBackend",
    "CACHES": {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    },
    "MIDDLEWARE": [
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
    ],
}


@pytest.fixture(scope="session", autouse=True)
def test_settings():
    with override_settings(**TEST_SETTINGS):
        yield
