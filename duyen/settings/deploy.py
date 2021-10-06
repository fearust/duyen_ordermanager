from .base import *

DEBUG = False
ALLOWED_HOSTS = ['3.35.173.174', 'duyen.shopping']

# Database
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

# Static, media
STATIC_URL = '/static_root/'
STATIC_ROOT = '/home/ubuntu/duyen/static_root'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/ubuntu/duyen/media'

DATA_UPLOAD_MAX_MEMORY_SIZE = 100*1024*1024