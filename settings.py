"""
Django settings for project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_NAME = os.path.basename(PROJECT_ROOT)
import sys
sys.path.append(os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dn#_0zjli7b9i8iz816e49++ftrxcdq!^go_^7$qv$bx_lma04'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = '{0}.urls'.format(PROJECT_NAME)

WSGI_APPLICATION = '{0}.wsgi.application'.format(PROJECT_NAME)


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'


SITE_ID = 1
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') + os.sep
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static') + os.sep
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
)

INSTALLED_APPS = (
    'grappelli',
    'filebrowser',
) + INSTALLED_APPS

INSTALLED_APPS += (
    # Dependencies
    'django.contrib.sites',
    'tagging',
    'pagination',
    'treemenus',
    'django_gravatar',
    'django_comments',
    # Apps
    'base',
    'player',
    'torrent',
    # Basic Apps
    'basic.blog',
    'basic.bookmarks',
    'basic.books',
    'basic.comments',
    #'basic.events',
    'basic.flagging',
    'basic.groups',
    'basic.inlines',
    #'basic.invitations',
    'basic.media',
    #'basic.messages',
    'basic.movies',
    'basic.music',
    'basic.people',
    'basic.places',
    'basic.profiles',
    'basic.relationships',
    'basic.tools',
)

COMMENTS_APP = 'basic.comments'
AUTH_PROFILE_MODULE = 'profiles.Profile'
