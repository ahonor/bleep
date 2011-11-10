from django.conf.urls.defaults import *

urlpatterns = patterns('registration.views',
    url(r'^profile/$', 'profile', name="registration_profile"),
    url(r'^tokens/$', 'tokens', name="registration_tokens"),
    url(r'^tokens/(?P<token_id>\d+)/delete/$', 'token_delete', name="registration_tokens_delete"),
)
