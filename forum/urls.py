from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('forum.views',
    url(r'^$', 'list_groupes', name='groupes'),
    url(r'^f/(?P<slug>[\-\d\w]+)/$', 'show_forum', name='showforum'),
    url(r'^t/(?P<slug>[\-\d\w]+)/$', 'show_thread', name='showthread'),
)

urlpatterns += patterns('forum.forms',
    url(r'^f/(?P<slug>[\-\d\w]+)/add/$', 'new_thread', name='newthread'),
    url(r'^t/(?P<slug>[\-\d\w]+)/add/$', 'new_message', name='newmessage'),
    url(r'^m/(?P<message_key>\w+)/testmessagemail/$', 'testmessagemail'),
    url(r'^f/(?P<slug>[\-\d\w]+)/subscribe/$', 'subscribe_forum', name='subscribeforum'),
    url(r'^f/(?P<slug>[\-\d\w]+)/unsubscribe/$', 'unsubscribe_forum', name='unsubscribeforum'),
    url(r'^t/(?P<slug>[\-\d\w]+)/subscribe/$', 'subscribe_thread', name='subscribethread'),
    url(r'^t/(?P<slug>[\-\d\w]+)/unsubscribe/$', 'unsubscribe_thread', name='unsubscribethread'),
)
