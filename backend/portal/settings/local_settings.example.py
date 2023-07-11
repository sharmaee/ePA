import os

from .database import DATABASES

WEBSITE_URL = "http://localhost:8080/"

# environment variables for deployment
DEBUG = int(os.environ.get("DJANGO_DEBUG", default=0))
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(" ")
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "***")
DB_CFG = {
    "USER": os.environ.get("SQL_USER", "prior_auth_user"),
    "HOST": os.environ.get("SQL_HOST", "127.0.0.1"),
    "PASSWORD": "***",
    "PORT": os.environ.get("SQL_PORT", "5432"),
    "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.postgresql"),
    "NAME": os.environ.get("SQL_DATABASE", "prior_auth_main"),
}

DATABASES['default'].update(DB_CFG)
