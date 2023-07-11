"""
Database settings
"""
import os

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# password is set in local settings
DATABASES = {
    "default": {
        "ATOMIC_REQUESTS": True,
        "USER": os.environ.get("SQL_USER", "prior_auth_user"),
        "HOST": os.environ.get("SQL_HOST", ""),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "***"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.environ.get("SQL_DATABASE", "prior_auth_main"),
    }
}
