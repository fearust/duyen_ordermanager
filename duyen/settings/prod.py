from .base import *

# home/ubuntu/duyen/venv/venv.env 에서 설정됨

DEBUG = False
ALLOWED_HOSTS = ['3.37.207.165']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'duyen',
        'USER': 'dbmasteruser',
        'PASSWORD': '+N*=|H5|_`f6R{-TVMLBwOd77J]gLp-,',
        'HOST': 'ls-9e9555d52f41681ed51b6d56b329ad40eaedac00.cbuobpiqxmfb.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}
