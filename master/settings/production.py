import dj_database_url

from . import *


DEBUG = False

TEMPLATE_DEBUG = False # debug template deactivate

#MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

SECRET_KEY = get_env_variable('SECRET_KEY','uszes#sc31015#5066ddgergèè_"84w&p=jji#$ikf#t*')

ALLOWED_HOSTS = ['localhost','pb.yoso.fr/'] # authorized hostname


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'OpenFoodFact',
        'USER': 'yohan',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
