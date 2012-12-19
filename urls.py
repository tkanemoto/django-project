from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stage.views.home', name='home'),
    # url(r'^stage/', include('stage.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Basic Apps dependencies
    (r'^comments/', include('django.contrib.comments.urls')),
    # Basic Apps
    url(r'^blog/', include('basic.blog.urls')),
    url(r'^bookmarks/', include('basic.bookmarks.urls')),
    url(r'^books/', include('basic.books.urls')),
    url(r'^blog-comments/', include('basic.events.urls')),
    url(r'^flagging/', include('basic.flagging.urls')),
    url(r'^groups/', include('basic.groups.urls')),
    #url(r'^inlines/', include('basic.inlines.urls')),
    url(r'^invitations/', include('basic.invitations.urls')),
    # url(r'^media/', include('basic.media.urls')),
    url(r'^media/photos', include('basic.media.urls.photos')),
    url(r'^media/videos', include('basic.media.urls.videos')),
    url(r'^messages/', include('basic.messages.urls')),
    url(r'^movies/', include('basic.movies.urls')),
    url(r'^music/', include('basic.music.urls')),
    url(r'^people/', include('basic.people.urls')),
    url(r'^places/', include('basic.places.urls')),
    url(r'^profiles/', include('basic.profiles.urls')),
    url(r'^relationships/', include('basic.relationships.urls')),
    # url(r'^tools/', include('basic.tools.urls')),
)
