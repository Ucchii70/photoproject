"""
Django settings for photoproject project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-!-ct!00lquf(g742x3*xp+(9hpd%54f%9)=a))bi^g^yju*dcj"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # photoアプリを追加
    "photo.apps.PhotoConfig",
    # accountsアプリを追加
    "accounts.apps.AccountsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "photoproject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "photoproject.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
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

# Userモデルの代わりにCustomUserモデルを使用
AUTH_USER_MODEL='accounts.CustomUser'

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "ja"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS=(os.path.join(BASE_DIR, 'static'),)

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# メール送信のためのクラスを設定
Email_BACKEND="django.core.mail.backends.smtp.EmailBackend"

# メールサーバーへの接続設定(GmailのSMTPサーバーを使用してメールを送信するための設定)
DEFAULT_FORM_EMAIL="mamemamesn@gmail.com"
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=587
EMAIL_HOST_USER="mamemamesn@gmail.com"
EMAIL_HOST_PASSWORD="xqukrnvkbmevrfnd"
EMAIL_USE_TLS="True"

# アップロードされたメディアファイルが保存されるディレクトリのパスを指定,プロジェクトのベースディレクトリ（BASE_DIR）に 'media' というサブディレクトリを結合して、メディアファイルが保存されるパスを作成
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Webページ上でメディアファイルにアクセスするためのURLを指定
MEDIA_URL = '/media/'

# 以下は一旦コメントアウト

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     # ログ出力フォーマットの設定
#     'formatters': {
#         'production': {
#             'format': '%(asctime)s [%(levelname)s] %(process)d %(thread)d '
#                       '%(pathname)s:%(lineno)d %(message)s'
#         },
#     },
#     # ハンドラの設定
#     'handlers': {
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': '/log/app.log',
#             'formatter': 'production',
#         },
#     },
#     # ロガーの設定
#     'loggers': {
#         # 自分で追加したアプリケーション全般のログを拾うロガー
#         '': {
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': False,
#         },
#         # Django自身が出力するログ全般を拾うロガー
#         'django': {
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': False,
#         },
#     },
# }