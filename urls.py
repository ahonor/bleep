from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^help/', include('help.urls')),
    (r'^bleeps/', include('bleeps.urls')),
    (r'^services/', include('services.urls')),
    (r'^parsers/', include('parsers.urls')),
    (r'^registration/', include('registration.urls')),
    (r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name="logout"),

    (r'^assets/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
)


from bleeps.feeds import LatestEntries
from bleeps.feeds import LatestComments

feeds = {
    'latest': LatestEntries,
    'comments':LatestComments
    }
urlpatterns += patterns('',
    (r'feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
       {'feed_dict':feeds}),
 )
