import configparser
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

config = configparser.ConfigParser()
config.read("poe/settings.ini")

SECRET_KEY = config.get("poe", "secret_key")

DEBUG = config["poe"].get("debug", False)


ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'trader.apps.TraderConfig',
    'django_admin_inline_paginator',
    'crispy_forms',
    'crispy_bootstrap4',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'poe.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Crispy forms version, using bootstrap
CRISPY_TEMPLATE_PACK = 'bootstrap4'

WSGI_APPLICATION = 'poe.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LEAGUE = "Sanctum"

POE_API = "https://poe.ninja/api/data"

ITEM_LIST = "itemoverview"

ITEM_PRISE = "itemhistory"

CURRENCY_LIST = "currencyoverview"

CURRENCY_PRICE = "currencyhistory"

POE_ITEM_URL = "https://poe.ninja/challenge"

# HEADERS = {'accept-encoding': 'gzip, deflate, br',
#            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
#            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
#                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

# Logger settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(name)s %(levelname)s %(asctime)s %(module)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'info-file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': 'logs/core-warning.log'
        }
    },
    'loggers': {
        'trader': {
            'level': 'DEBUG',
            'handlers': ['console', 'info-file']
        }
    }
}
