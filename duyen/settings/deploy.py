from .base import *

DEBUG = False
ALLOWED_HOSTS = ['3.37.207.165', 'duyen.shopping']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'duyen',
        'USER': 'dbmasteruser',
        'PASSWORD': 'HCyE{AZa71R^f.L>4~5Sn$X65nW0MIUj',
        'HOST': 'ls-750c7b15de15d79a3a832fc17bd09b187d8c560e.cbuobpiqxmfb.ap-northeast-2.rds.amazonaws.com',
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