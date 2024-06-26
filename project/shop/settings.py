"""
Django settings for shop project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os.path
from pathlib import Path

import redis

from .config import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
CONFIG = config()
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG.django_settings.secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.django_settings.debug

ALLOWED_HOSTS = CONFIG.django_settings.hosts

CSRF_TRUSTED_ORIGINS=CONFIG.django_settings.trusted_origins
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    'apps.shop_app.apps.ShopAppConfig',
    'apps.cart.apps.CartConfig',
    'apps.user.apps.UserConfig',
    'apps.likes.apps.LikesConfig',
    'apps.orders.apps.OrdersConfig',
    'apps.payment.apps.PaymentConfig',
    'apps.coupons.apps.CouponsConfig',

    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.cart.context_processors.cart',
                'apps.likes.context_processors.likes',
            ],
        },
    },
]

WSGI_APPLICATION = 'shop.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': CONFIG.db.name,
        'USER': CONFIG.db.user,
        'PASSWORD': CONFIG.db.password,
        'HOST': CONFIG.db.host,
        'PORT': CONFIG.db.port
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

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


LOGIN_URL = 'user:login'
LOGOUT_REDIRECT_URL = 'user:logout'

REDIS_HOST = CONFIG.redis.host
REDIS_PORT = CONFIG.redis.port
REDIS_DB = CONFIG.redis.db

CART_SESSION_ID = 'cart'
LIKES_SESSION_ID = 'likes'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = CONFIG.smtp.email_host
EMAIL_HOST_USER = CONFIG.smtp.email_host_user
EMAIL_HOST_PASSWORD = CONFIG.smtp.email_host_password
EMAIL_PORT = CONFIG.smtp.email_port
EMAIL_USE_TLS = True

GOOGLE_RECAPTCHA_SECRET_KEY = CONFIG.recaptcha.secret_key
GOOGLE_RECAPTCHA_PUBLIC_KEY = CONFIG.recaptcha.public_key

CELERY_BROKER_URL = CONFIG.celery.broker_url

STRIPE_SECRET_KEY = CONFIG.stripe.secret_key
STRIPE_PUBLIC_KEY = CONFIG.stripe.pub_key
STRIPE_WEBHOOK_SECRET = CONFIG.stripe.webhook_secret
