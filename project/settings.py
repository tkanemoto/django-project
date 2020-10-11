from .settings_default import *

import os
import sys
sys.path.append(os.path.join(BASE_DIR, 'apps'))

TEMPLATES[0]['DIRS'] = [
	os.path.join(BASE_DIR, 'templates'),
]

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_ROOT = os.path.join(BASE_DIR, 'static')
COMPRESS_OUTPUT_DIR = 'compressed'
COMPRESS_CSS_FILTERS = [
    #'compressor.filters.css_default.CssAbsoluteFilter',
    #'compressor.filters.datauri.CssDataUriFilter',
    'compressor.filters.css_default.CssRelativeFilter',
    'compressor.filters.cssmin.rCSSMinFilter',
]
COMPRESS_DATA_URI_MAX_SIZE = 1000000

ENABLE_JET = bool(os.environ.get('ENABLE_JET', ''))

if ENABLE_JET:
    INSTALLED_APPS = [
        'jet.dashboard',
        'jet',
        'jet_django',
    ] + INSTALLED_APPS

INSTALLED_APPS += [
    #'portfolios',
    'storages',
    'ordered_model',
]

INSTALLED_APPS += [
    # Dependencies
    'django.contrib.sites',
    'django.contrib.humanize',
    'tagging',
    'treemenus',
    'django_gravatar',
    'django_comments',
    # Apps
    'base',
    'player',
    'dj_torrent',
    # Basic Apps
    'basic.blog',
    #'basic.bookmarks',
    #'basic.books',
    'basic.comments',
    #'basic.events',
    #'basic.flagging',
    #'basic.groups',
    'basic.inlines',
    #'basic.invitations',
    #'basic.media',
    #'basic.messages',
    #'basic.movies',
    'basic.music',
    'basic.people',
    #'basic.places',
    'basic.profiles',
    #'basic.relationships',
    'basic.tools',
    # Bingo
    #'bingo',
    #'jquery',
    #'colorful',
    #'registration',
    # Others
    'compressor',
]

COMMENTS_APP = 'basic.comments'
AUTH_PROFILE_MODULE = 'profiles.Profile'

SITE_ID = 1

MIDDLEWARE += [
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
]

TEMPLATE_DEBUG = DEBUG

if DEBUG:
    MEDIA_ROOT = BASE_DIR
    MEDIA_URL = '/media/'
    ALLOWED_HOSTS = ['*']

# TEMPLATES[0]['OPTIONS']['context_processors'] += [
#     'bingo.context_processors.bingo',
# ]
# BINGO_GAME_HARD_TIMEOUT = 1440
# BINGO_GAME_SOFT_TIMEOUT = 360
# BINGO_TWEETBUTTON_TEXT = None
# BINGO_FONT_PATH = os.path.join(BASE_DIR, 'static', 'fonts', 'Roboto-Regular.ttf')

ADMIN_SITE_HEADER = 'Django administration'

_FILE_UPLOAD_HANDLERS = [
    'portfolios.uploadhandlers.CompressImageUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

FILE_UPLOAD_MAX_MEMORY_SIZE = 262144000
