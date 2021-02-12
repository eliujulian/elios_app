"""
Django settings for elios_app project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
import sys
from pathlib import Path
import gunicorn
import django_heroku
from django import db

# Build paths inside the project like this: os.path.join(BASE_DIR, "subdir").
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY_ELIOSAPP']

# SECURITY WARNING: don't run with debug turned on in production!
if str(BASE_DIR).startswith("C:\\Users"):  # Enable debug when run local
    DEBUG = True
    BASE_URL = "http://127.0.0.1:8000"
else:  # Heroku
    DEBUG = False
    BASE_URL = "http://elios-app.herokuapp.com"

ALLOWED_HOSTS = ['127.0.0.1', 'elios-app.herokuapp.com']

# Application definition

INSTALLED_APPS = [
    'core',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'health',
    'personality',
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

ROOT_URLCONF = 'elios_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/templates'],
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

WSGI_APPLICATION = 'elios_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        "NAME": os.path.join(BASE_DIR, "db.sqlite3")
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
# STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

AUTH_USER_MODEL = 'core.User'

# E-Mail Settings
EMAIL_HOST = os.environ['ELIOSAPP_EMAIL_HOST']
EMAIL_HOST_PASSWORD = os.environ['ELIOSAPP_EMAIL_HOST_PASSWORD']
EMAIL_HOST_USER = os.environ['ELIOSAPP_EMAIL_HOST_USER']
MAIL_PORT = 25
EMAIL_SUBJECT_PREFIX = ""


if "test" not in sys.argv:  # No testing with live database, using sqlite when running tests
    django_heroku.settings(locals())  # Comment out to use local sqlite3.db
    pass

print("Running with database - HOST/NAME: ",
      db.connections.databases['default'].get('HOST'),
      db.connections.databases['default'].get('NAME'))
print("Basedir:", BASE_DIR)

# App Dashboard
ALLOW_SENDING_CONFIRMATION_EMAILS = True

if not ALLOW_SENDING_CONFIRMATION_EMAILS:
    print("WARNING: No sending of confirmation E-Mails")

CHECK_CREATE_GROUPS = True
