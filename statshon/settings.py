"""
Django settings for statshon project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import environ
import django_heroku

from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env()

READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / '.env'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('DJANGO_SECRET_KEY', default='9=52+$nm-if$d$sc%+c_-sp$2@cbkeq#cn15kmaeu&ecyy&csg')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', default=True)

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'things',
    'honauth',
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

ROOT_URLCONF = 'statshon.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'honauth.context_processors.hon_app_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'statshon.wsgi.application'

LOGIN_URL = reverse_lazy('home')

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASE_NAME = env.str('DJANGO_DB_NAME', default='./db.sqlite3')

DATABASES = {
    'default': {
        'ENGINE': env.str('DJANGO_DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': DATABASE_NAME,
        'HOST': env.str('DJANGO_DB_HOSTNAME', default='localhost'),
        'PORT': env.int('DJANGO_DB_PORT', default=5433),
        'USER': env.str('DJANGO_DB_USERNAME', default=''),
        'CONN_MAX_AGE': None,
        'PASSWORD': env.str('DJANGO_DB_PASSWORD', default=''),
    }
}

CSRF_TRUSTED_ORIGINS = env.list('DJANGO_TRUSTED_ORIGINS', default=['*'])


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

STORAGES = {
    'default': {
        'BACKEND': env.str('DJANGO_STORAGE_BACKEND', default='django.core.files.storage.FileSystemStorage'),
        'OPTIONS': {
            'location': '/media',
            'base_url': '/media/',
        },
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media_data')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ADMIN_PATH = env.str('DJANGO_ADMIN_PATH', default='admin')

# Dropbox related settings and stuff
# set 'storages.backends.dropbox.DropboxStorage' as default django storage backend

DROPBOX_OAUTH2_TOKEN = env.str('DROPBOX_OAUTH2_TOKEN', default='')

DROPBOX_APP_KEY = env.str('DROPBOX_APP_KEY', default='')

DROPBOX_APP_SECRET = env.str('DROPBOX_APP_SECRET', default='')

DROPBOX_OAUTH2_REFRESH_TOKEN = env.str('DROPBOX_OAUTH2_REFRESH_TOKEN', default='')

DROPBOX_ROOT_PATH = env.str('DROPBOX_ROOT_PATH', default='/')

DROPBOX_TIMEOUT = env.str('DROPBOX_TIMEOUT', default=100)

DROPBOX_WRITE_MODE = env.str('DROPBOX_WRITE_MODE', default='add')

# Heroku related stuff
django_heroku.settings(locals(), staticfiles=False)

# Default populated superuser
DEFAULT_SUPERUSER_NAME = env.str('DEFAULT_SUPERUSER_NAME', default='')
DEFAULT_SUPERUSER_PASS = env.str('DEFAULT_SUPERUSER_PASS', default='')
