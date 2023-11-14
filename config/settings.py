from __future__ import annotations

import re
import socket
import sys
from pathlib import Path

import django_stubs_ext
import sentry_sdk
from django.template import base
from environs import Env
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from core.navigation import NavItem
from core.redirects import Redirects
from core.sentry import sentry_traces_sampler
from core.social import SocialItem

# 0. Setup

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

env = Env()
env.read_env(Path(BASE_DIR, ".env").as_posix())

# Monkeypatching Django, so stubs will work for all generics,
# see: https://github.com/typeddjango/django-stubs
django_stubs_ext.monkeypatch()

# Monkeypatching Django templates, to support multiline template tags
base.tag_re = re.compile(base.tag_re.pattern, re.DOTALL)

# We should strive to only have two possible runtime scenarios: either `DEBUG`
# is True or it is False. `DEBUG` should be only true in development, and
# False when deployed, whether or not it's a production environment.
DEBUG = env.bool("DEBUG", default=False)

# `STAGING` is here to allow us to tweak things like urls, smtp servers, etc.
# between staging and production environments, **NOT** for anything that `DEBUG`
# would be used for.
STAGING = env.bool("STAGING", default=False)

# 1. Django Core Settings
# https://docs.Assets.com/en/4.0/ref/settings/

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"] if DEBUG else ["localhost"])

ASGI_APPLICATION = "assets.asgi.application"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
    if DEBUG
    else {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache",
    }
}

DATABASES = {
    "default": env.dj_db_url(
        "DATABASE_URL",
        default="sqlite:///db.sqlite3",
        conn_max_age=600,  # 10 minutes
        conn_health_checks=True,
    )
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS = [
    # First Party
    "blog",
    "core",
    "core.admin",
    "core.admin.default",
    "users",
    # Third Party
    "anymail",
    "crispy_forms",
    "crispy_tailwind",
    "django_browser_reload",
    "django_extensions",
    "django_htmx",
    "django_tailwind_cli",
    # "django_watchfiles",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.migrations",
    "heroicons",
    "neapolitan",
    "simple_history",
    # Django
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]
if DEBUG:
    INSTALLED_APPS = [
        "debug_toolbar",
        "whitenoise.runserver_nostatic",
    ] + INSTALLED_APPS

if DEBUG:
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]

LANGUAGE_CODE = "en-us"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "plain_console": {
            "format": "%(levelname)s %(message)s",
        },
        "verbose": {
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        },
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["stdout"],
            "level": env("DJANGO_LOG_LEVEL", default="INFO"),
        },
        "blog": {
            "handlers": ["stdout"],
            "level": env("BLOG_LOG_LEVEL", default="INFO"),
        },
        "core": {
            "handlers": ["stdout"],
            "level": env("CORE_LOG_LEVEL", default="INFO"),
        },
        "users": {
            "handlers": ["stdout"],
            "level": env("USERS_LOG_LEVEL", default="INFO"),
        },
    },
}

# https://docs.djangoproject.com/en/dev/topics/http/middleware/
# https://docs.djangoproject.com/en/dev/ref/middleware/#middleware-ordering
MIDDLEWARE = [
    # should be first
    "core.redirects.middleware.redirect_middleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # order doesn't matter
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "django_flyio.middleware.FlyResponseMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    # should be last
    "django.middleware.cache.FetchFromCacheMiddleware",
]
if DEBUG:
    MIDDLEWARE.remove("django.middleware.cache.UpdateCacheMiddleware")
    MIDDLEWARE.remove("django.middleware.cache.FetchFromCacheMiddleware")

    MIDDLEWARE.insert(
        MIDDLEWARE.index("django.middleware.common.CommonMiddleware") + 1,
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    )

ROOT_URLCONF = "config.urls"

SECRET_KEY = env(
    "SECRET_KEY",
    default="eZPdvuAaLrVY8Kj3DG2QNqJaJc4fPp6iDgYneKN3fkNmqgkcNnoNLkFe3NCRXqW",
)

SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG

SECURE_HSTS_PRELOAD = not DEBUG

# 10 minutes to start with, will increase as HSTS is tested
SECURE_HSTS_SECONDS = 0 if DEBUG else 600

# https://noumenal.es/notes/til/django/csrf-trusted-origins/
# https://fly.io/docs/reference/runtime-environment/#x-forwarded-proto
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = not DEBUG

SILENCED_SYSTEM_CHECKS = [
    # Pending new release of django-debug-toolbar
    # See jazzband/django-debug-toolbar#1780
    "debug_toolbar.W006",
]

SITE_ID = 1

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# https://nickjanetakis.com/blog/django-4-1-html-templates-are-cached-by-default-with-debug-true
DEFAULT_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

CACHED_LOADERS = [("django.template.loaders.cached.Loader", DEFAULT_LOADERS)]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            Path(BASE_DIR, "templates"),
        ],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.metadata",
            ],
            "debug": DEBUG,
            "loaders": [
                (
                    "template_partials.loader.Loader",
                    DEFAULT_LOADERS if DEBUG else CACHED_LOADERS,
                )
            ],
        },
    },
]

TIME_ZONE = "America/Chicago"

USE_I18N = False

USE_TZ = True

WSGI_APPLICATION = "config.wsgi.application"

# 2. Django Contrib Settings

# django.contrib.auth
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "users.User"

# django.contrib.staticfiles
STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static" / "dist",
    BASE_DIR / "static" / "public",
]

# 3. Third Party Settings

# django-anymail
ANYMAIL = {
    "MAILGUN_API_KEY": env("MAILGUN_API_KEY", default=""),
    "MAILGUN_SENDER_DOMAIN": env("MAILGUN_SENDER_DOMAIN", default=""),
}

# django-cripsy-forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"

# django-debug-toolbar
DEBUG_TOOLBAR_CONFIG = {
    "ROOT_TAG_EXTRA_ATTRS": "hx-preserve",
}

# django-tailwind-cli
TAILWIND_CLI_CONFIG_FILE = "tailwind.config.cjs"

TAILWIND_CLI_SRC_CSS = "static/public/tailwind.css"

# sentry
if not DEBUG or env.bool("ENABLE_SENTRY", default=False):
    sentry_sdk.init(
        dsn=env("SENTRY_DSN", default=None),
        environment=env("SENTRY_ENV", default=None),
        integrations=[
            DjangoIntegration(),
            LoggingIntegration(event_level=None, level=None),
        ],
        traces_sampler=sentry_traces_sampler,
        send_default_pii=True,
    )

# 4. Project Settings

ENABLE_ADMIN_2FA = not DEBUG or env.bool("ENABLE_ADMIN_2FA", default=False)

REDIRECTS = Redirects.from_json(BASE_DIR / "redirects.json")

NAVIGATION = [
    NavItem(title="Home", url="index"),
    NavItem(title="Blog", url="blog:index"),
]

SOCIALS = [
    SocialItem(
        title="Mastodon",
        url="https://joshthomas.dev/@josh",
        icon_template="partials/mastodon.svg",
    ),
    SocialItem(
        title="GitHub",
        url="https://github.com/joshuadavidthomas",
        icon_template="partials/github.svg",
    ),
    SocialItem(
        title="LinkedIn",
        url="https://www.linkedin.com/in/joshua-thomas-b1745a16/",
        icon_template="partials/linkedin.svg",
    ),
    SocialItem(
        title="RSS",
        url="blog:feed",
        icon_template="partials/rss.svg",
    ),
]

STEAM = {
    "API_KEY": env("STEAM_API_KEY", default=""),
    "USER_ID": env("STEAM_USER_ID", default=""),
    "ACCOUNT_ID": env("STEAM_ACCOUNT_ID", default=""),
}

MINIFLUX = {
    "URL": env("MINIFLUX_URL", default=""),
    "API_KEY": env("MINIFLUX_API_KEY", default=""),
}
