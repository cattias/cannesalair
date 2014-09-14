from core.feeds import LatestLogEntriesFeed, LatestAttributeLogEntriesFeed
from django.conf.urls.defaults import patterns, url

feeds = {
    'latestlog': LatestLogEntriesFeed,
    'latestattributelog': LatestAttributeLogEntriesFeed,
}

urlpatterns = patterns('',
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}, name="feedcore"),
    url(r'^hgpullu/$', 'core.views.hgpullu', name="hgpullu"),
    url(r'^files/$', 'core.views.files', name="files"),
    url(r'^upload/$', 'core.views.upload', name="uploadfiles"),
    url(r'^json/$', 'core.views.get_json_listfiles', name='getjsonlistfiles'),
    url(r'^deletefile/$', 'core.views.deletefile', name='deletefile'),
)