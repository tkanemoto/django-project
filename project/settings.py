from settings_default import *

import sys
sys.path.append(os.path.join(BASE_DIR, 'apps'))

TEMPLATES[0]['DIRS'] = [
	os.path.join(BASE_DIR, 'templates'),
]

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

INSTALLED_APPS += (
    'portfolios',
    'storages',
    'ordered_model',
)

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
)

COMMENTS_APP = 'basic.comments'
AUTH_PROFILE_MODULE = 'profiles.Profile'

SITE_ID = 1

TEMPLATE_DEBUG = DEBUG

if DEBUG:
    MEDIA_ROOT = BASE_DIR
    MEDIA_URL = '/media/'