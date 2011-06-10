

DEBUG = True
TEMPLATE_DEBUG = DEBUG

import os

SECRET_KEY = 'lksdkfpoi*(D*3uff0@_#*4dhfksjdfla48;a9dfy'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'database',
    'south',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

# This test runner captures stdout and associates tracebacks with their
# corresponding output. Helps a lot with print-debugging.

ADMIN_MEDIA_PREFIX = '/media/admin/'
STATICFILES_ROOT = os.path.join(os.path.dirname(__file__), '_generated_media')
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), 'public/static'),
)
STATIC_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'public/files')
MEDIA_URL = '/files/'
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

ROOT_URLCONF = 'urls'

SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': './sqlite.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

