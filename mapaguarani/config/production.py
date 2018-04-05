'''
Production Configurations
- Use djangosecure
- Use Amazon's S3 for storing static files and uploaded media
- Use sendgrid to send emails
- Use MEMCACHIER on Heroku
'''
from __future__ import absolute_import, unicode_literals

from .common import *  # noqa

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = env("SITE_ID", default=1)

# END SITE CONFIGURATION

INSTALLED_APPS += ('gunicorn', )
INSTALLED_APPS += ('raven.contrib.django.raven_compat', )

MEDIA_ROOT = env('MEDIA_ROOT', default='/app/staticfiles/media')
STATIC_ROOT = env('STATIC_ROOT', default='/app/staticfiles/static')
# STATICFILES_DIRS = env('STATICFILES_DIRS')

COMPRESS_OFFLINE = True
COMPRESS_ROOT = env('COMPRESS_ROOT', default=STATIC_ROOT)
COMPRESS_OUTPUT_DIR = ''

# EMAIL
# ------------------------------------------------------------------------------
# DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL',
#                          default='')
EMAIL_HOST = env("DJANGO_EMAIL_HOST", default='smtp.sendgrid.com')
# EMAIL_HOST_PASSWORD = env("SENDGRID_PASSWORD")
# EMAIL_HOST_USER = env('SENDGRID_USERNAME')
# EMAIL_PORT = env.int("EMAIL_PORT", default=587)
# EMAIL_SUBJECT_PREFIX = env("EMAIL_SUBJECT_PREFIX", default='[{{cookiecutter.project_name}}] ')
# EMAIL_USE_TLS = True
# SERVER_EMAIL = EMAIL_HOST_USER

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

# Sentry Configuration
if env('DJANGO_SENTRY_DSN', default=False):
    SENTRY_DSN = env('DJANGO_SENTRY_DSN')
    SENTRY_CLIENT = env('DJANGO_SENTRY_CLIENT', default='raven.contrib.django.raven_compat.DjangoClient')
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry', ],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                        '%(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console', ],
                'propagate': False,
            },
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console', ],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console', ],
                'propagate': False,
            },
            'django.security.DisallowedHost': {
                'level': 'ERROR',
                'handlers': ['console', 'sentry', ],
                'propagate': False,
            },
        },
    }

# Your production stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
