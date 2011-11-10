from django.conf.urls.defaults import *

urlpatterns = patterns('services.views',
    url(r'^$','list', name="services_list"),
    url(r'^(?P<service_type>\w+)/$', 'show', name="services_show"),
    url(r'^(?P<service_type>\w+)/perform$', 'perform', name="services_perform"),
)
