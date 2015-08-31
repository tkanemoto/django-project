from django.conf.urls import patterns, include, url
from django.contrib import admin

from filebrowser.sites import site as filebrowser_site

urlpatterns = patterns('',
    url(r'^admin/filebrowser/', include(filebrowser_site.urls)),
    url(r'^admin/', include(admin.site.urls)),

    # Basic Apps
    url(r'^blog/', include('basic.blog.urls')),
    #url(r'^bookmarks/', include('basic.bookmarks.urls')),
    #url(r'^books/', include('basic.books.urls')),
    url(r'^comments/', include('basic.comments.urls')),
    #url(r'^events/', include('basic.events.urls')),
    #url(r'^flagging/', include('basic.flagging.urls')),
    #url(r'^groups/', include('basic.groups.urls')),
    #url(r'^invitations/', include('basic.invitations.urls')),
    #url(r'^photos', include('basic.media.urls.photos')),
    #url(r'^videos', include('basic.media.urls.videos')),
    #url(r'^messages/', include('basic.messages.urls')),
    #url(r'^movies/', include('basic.movies.urls')),
    #url(r'^music/', include('basic.music.urls')),
    #url(r'^people/', include('basic.people.urls')),
    #url(r'^places/', include('basic.places.urls')),
    url(r'^users/', include('basic.profiles.urls')),
    #url(r'^relationships/', include('basic.relationships.urls')),
    # url(r'^tools/', include('basic.tools.urls')),
    # Apps
    url(r'^player/', include('player.urls')),
    url(r'^torrent/', include('torrent.urls')),
    url(r'^', include('base.urls')),
    # Login
    url('^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
)

from django.conf import settings

from django.contrib.auth.decorators import login_required, user_passes_test
def media_access(user):
    return user.is_staff or \
        user.groups.filter(name__in=['media-access', 'admins']).exists()

#if settings.DEBUG:
if True:
    from django.views.static import serve
    if settings.MEDIA_URL.startswith('/'):
        media_url = settings.MEDIA_URL[1:]
        urlpatterns += patterns(
            '',
            (r'^%s(?P<path>.*)$' % media_url,
            user_passes_test(media_access)(serve),
            {'document_root': settings.MEDIA_ROOT})
        )
