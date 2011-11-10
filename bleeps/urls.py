from django.conf.urls.defaults import *

urlpatterns = patterns('bleeps.views',
    url(r'^$', 'bleeps', name='bleeps'),
    url(r'^bleep$','add', name='bleep_add'),
    url(r'^digest/$','digest', name='digest'),
    url(r'^search/$', 'search', name='search'),
    url(r'^(?P<bleep_id>\d+)/$', 'show', name='bleep_show'),
    url(r'^(?P<bleep_id>\d+)/edit$', 'edit', name='bleep_edit'),
    url(r'^(?P<bleep_id>\d+)/send$', 'send', name='bleep_send'),
    url(r'^(?P<bleep_id>\d+)/update$', 'update', name='bleep_update'),
    url(r'^(?P<bleep_id>\d+)/comment$', 'comment', name='bleep_comment'),
)
