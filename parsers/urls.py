from django.conf.urls.defaults import *

urlpatterns = patterns('parsers.views',
    (r'^(?P<parser_type>\w+)/$', 'show'),
    (r'^(?P<parser_type>\w+)/perform$', 'perform'),
)

