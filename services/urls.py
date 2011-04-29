from django.conf.urls.defaults import *

urlpatterns = patterns('services.views',
    (r'^$','list'),
    (r'^(?P<service_type>\w+)/$', 'show'),
    (r'^(?P<service_type>\w+)/perform$', 'perform'),
)

