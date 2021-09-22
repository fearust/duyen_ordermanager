from pathlib import Path
import os
import json
from django.core.exceptions import ImproperlyConfigured


# base dir
BASE_DIR = Path(__file__).resolve().parent.parent

# secret value
with open(BASE_DIR / "secret.json") as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = f"Set the {setting} enviroment variable"
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_secret("SECRET_KEY")


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'ordermanager.apps.OrdermanagerConfig',
    'common.apps.CommonConfig',
    'imagekit',
    'simplemde',
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

ROOT_URLCONF = 'duyen.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'duyen.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'duyen',
        'USER': 'dbmasteruser',
        'PASSWORD': '+N*=|H5|_`f6R{-TVMLBwOd77J]gLp-,',
        'HOST': 'ls-9e9555d52f41681ed51b6d56b329ad40eaedac00.cbuobpiqxmfb.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}

# Password validation

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


# language
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# static, media
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATIC_URL = '/static_root/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = '/home/ubuntu/duyen/static_root'
MEDIA_ROOT = '/home/ubuntu/duyen/media'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/common/login/'

SIMPLEMDE_OPTIONS = {
    'placeholder': '내용을 입력하세요',
    'status': False,
    'autosave': {'enabled': True},
    'spellChecker': False,
}

DEBUG = False
ALLOWED_HOSTS = ['3.37.207.165', 'duyen.shopping']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'duyen',
        'USER': 'dbmasteruser',
        'PASSWORD': '+N*=|H5|_`f6R{-TVMLBwOd77J]gLp-,',
        'HOST': 'ls-9e9555d52f41681ed51b6d56b329ad40eaedac00.cbuobpiqxmfb.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}
