from pathlib import Path
import sys
import os


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-yln#$3au46t_(ojsqtp3s@5(no*3o4-89$!@4#v5t-5iv!k+w)'

DEBUG = True

ALLOWED_HOSTS = []
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'apps'))

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework'
]
PROJECT_APPS = [
    'apps.main.apps.MainConfig'
]
INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'settings.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'settings.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'blog_basee', 
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': '127.0.0.1', 
        'PORT': '5432',
    }
}



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



LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Asia/Almaty'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATIC_ROOT = 'static/'

MEDIA_URL = 'media/'

MEDIA_ROOT = 'media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
