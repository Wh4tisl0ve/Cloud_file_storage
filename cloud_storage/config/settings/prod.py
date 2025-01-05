from decouple import Config, RepositoryEnv

from .base import *


config = Config(RepositoryEnv(".env.prod"))

DEBUG = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(" ")

SECRET_KEY = config("SECRET_KEY")

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT"),
        "TEST": {
            "NAME": f"{config("POSTGRES_DB")}_test",
        },
    }
}

STATIC_ROOT = BASE_DIR / "static/"
STATIC_URL = "/static/"
