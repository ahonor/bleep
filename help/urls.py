from django.conf.urls.defaults import *

urlpatterns = patterns('help.views',
    url(r'^$', 'index', name="help"),
)

