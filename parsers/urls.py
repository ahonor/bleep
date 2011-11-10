from django.conf.urls.defaults import *

urlpatterns = patterns('parsers.views',
    url(r'^(?P<parser_type>\w+)/$', 'show', name="parsers_show"),
    url(r'^(?P<parser_type>\w+)/perform$', 'perform', name="parsers_perform"),
)

