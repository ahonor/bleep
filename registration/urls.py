from django.conf.urls.defaults import *

urlpatterns = patterns('registration.views',
    (r'^profile/$', 'profile'),
    (r'^tokens/$', 'tokens'),
    (r'^tokens/(?P<token_id>\d+)/delete/$', 'token_delete'),
)
