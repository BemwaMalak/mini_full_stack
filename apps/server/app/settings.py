import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
###############################################
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True

RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "False") == "True"

# Application definition
###############################################
INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "rest_framework",
    "app",
    "authentication",
    "medication",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "authentication.middlewares.ExtractCsrfMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]

ROOT_URLCONF = "app.urls"
WSGI_APPLICATION = "app.wsgi.application"

# Database configuration
###############################################
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DATABASE_NAME"),
        "USER": os.getenv("DATABASE_USERNAME"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "HOST": os.getenv("DATABASE_HOST"),
        "PORT": os.getenv("DATABASE_PORT_NUMBER"),
        "OPTIONS": {"pool": True},
    },
    "test": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("TEST_DATABASE_NAME"),
        "USER": os.getenv("TEST_DATABASE_USERNAME"),
        "PASSWORD": os.getenv("TEST_DATABASE_PASSWORD"),
        "HOST": os.getenv("TEST_DATABASE_HOST"),
        "PORT": os.getenv("TEST_DATABASE_PORT_NUMBER"),
    },
}

# Use test database configuration when running tests
if "test" in sys.argv or "test_coverage" in sys.argv:
    DATABASES["default"] = DATABASES["test"]

# Authentication settings
###############################################
AUTH_USER_MODEL = "authentication.User"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Django REST framework configuration
###############################################
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "EXCEPTION_HANDLER": "app.utils.exception_handler",
}

# Static and media files
###############################################
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Localization settings
###############################################
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Django CORS headers configuration
###############################################
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
