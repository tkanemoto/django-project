from django.conf.urls import *

from .views import *

urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/$', view=PageDetail.as_view(), name='portfolios-page'),
    url(r'^$', view=Home.as_view(), name='portfolios-home'),
]
