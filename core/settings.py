"""
Django settings for core project.

MAINTAINER: Eri Adeodu (@50-Course)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import environ
from celery.schedules import crontab

env = environ.Env(DEBUG=(bool, False))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG")

ALLOWED_HOSTS = env.str("DJANGO_ALLOWED_HOSTS").split(" ")

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_celery_beat",
    "drf_spectacular",
    "django_filters",
]

if DEBUG is True:
    DJANGO_APPS.insert(-2, "whitenoise.runserver_nostatic")

LOCAL_APPS = ["api.apps.ApiConfig", "newsapp.apps.NewsappConfig"]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#     }
# }
# DATABASES["default"]["HOST"] = env("DB_PROD_HOST")
# DATABASES["default"]["USER"] = env("DB_PROD_USER")
# DATABASES["default"]["NAME"] = env("DB_PROD_NAME")
# DATABASES["default"]["PASSWORD"] = env("DB_PROD_PASSWORD")
# DATABASES["default"]["PORT"] = env("DB_PROD_PORT")

# # Testing should be done in SQLite
# if "test" in sys.argv or r"test\_coverage" in sys.argv:
#     DATABASES["default"]["ENGINE"] = "django.db.backends.sqlite3"
#     DATABASES["default"]["NAME"] = env("TEST_DB_NAME")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIR = [BASE_DIR / "staticfiles"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# # HTTP/SSL & SECURITY
# SECURE_SSL_REDIRECT = envcls.get_stories()("DJANGO_SECURE_SSL_REDIRECT", default=True)
# SESSION_COOKIE_HTTP_ONLY = True
# # # HTTPS Strict Transport Security
# SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=False)
# SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
#     "DJANGO_HSTS_INCLUDE_SUBDOMAINS", default=False
# )
# SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=0)

# Hacker News Endpoint
HACKER_NEWSAPI_URI = "https://hacker-news.firebaseio.com/v0"
"""Official Hacker News API."""

# Celery Configuration
CELERY_BEAT_SCHEDULE = {
    "sync_db": {
        "task": "api.tasks.sync_db",
        "schedule": crontab(minute="*/1"),
    },
}

CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")
CELERY_BACKEND = env.str("CELERY_BACKEND")

# DRF
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ],
}


# SPECTACULAR
SPECTACULAR_SETTINGS = {
    "TITLE": "Hacker News API",
    "DESCRIPTION": "An unofficial distribution of Hacker News API. ",
    "VERSION": "2.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "DEFAULT_GENERATOR_CLASS": "drf_spectacular.generators.SchemaGenerator",
    "CONTACT": {"name": "Eri", "url": "https://linkedin.com/in/symply-eri/"},
}

# # Custom User
# AUTH_USER_MODEL = 'api.User'o
