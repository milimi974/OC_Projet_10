import dj_database_url

from .settings import *


DEBUG = False

TEMPLATE_DEBUG = False# debug template deactivate

DATABASES['default'] = dj_database_url.config()

MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# SECRET_KEY = get_env_variable('SECRET_KEY')

ALLOWED_HOSTS = ['p8pb.herokuapp.com'] # authorized hostname

