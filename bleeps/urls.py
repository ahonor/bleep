from django.conf.urls.defaults import *

urlpatterns = patterns('bleeps.views',
    (r'^$', 'bleeps'),
    (r'^bleep$','add'),
    (r'^(?P<bleep_id>\d+)/$', 'show'),
    (r'^(?P<bleep_id>\d+)/edit$', 'edit'),
    (r'^(?P<bleep_id>\d+)/update$', 'update'),
    (r'^(?P<bleep_id>\d+)/send$', 'send'),
    (r'^(?P<bleep_id>\d+)/comment$', 'comment'),
    (r'^search/$', 'search'),                       
    (r'^digest/$','digest'),
)
