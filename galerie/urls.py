from galerie.feeds import LatestGaleriesFeed
from django.conf.urls.defaults import patterns, url

feeds = {
    'latest': LatestGaleriesFeed,
}

# feeds
urlpatterns = patterns('',
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}, name="feedgalerie"),
)

urlpatterns += patterns('galerie.views',
    url(r'^$', 'list_galeries', name="galeries"),
    url(r'^link/$', 'link_galerie', name='linkgalerie'),
    url(r'^add/$', 'add_galerie', name='addgalerie'),
    url(r'^image/(?P<imagehash>.*)/$', 'view_image', name='viewimage'),
    url(r'^upload/$', 'upload_photos', name='uploadphotos'),
    url(r'^(?P<slug>[\-\d\w]+)/image/(?P<image_id>\d+)/delete/$', 'delete_image', name='deleteimage'),
    url(r'^(?P<slug>[\-\d\w]+)/edit/$', 'edit_galerie', name='editgalerie'),
    url(r'^(?P<slug>[\-\d\w]+)/upload/$', 'upload_galerie', name='uploadgalerie'),
    url(r'^(?P<slug>[\-\d\w]+)/download/$', 'download_galerie', name='downloadgalerie'),
    url(r'^(?P<slug>[\-\d\w]+)/downloadend/$', 'downloadend_galerie', name='downloadendgalerie'),
    url(r'^(?P<slug>[\-\d\w]+)/updatephotos/$', 'update_photos', name='updatephotos'),
    url(r'^(?P<slug>[\-\d\w]+)/delete/$', 'delete_galerie', name='deletegalerie'),
    url(r'^(?P<slug>[\-\d\w]+)/subscribe/$', 'subscribe_galerie_imgur', name='subscribegalerie'),
    url(r'^(?P<slug>[\-\d\w]+)/unsubscribe/$', 'unsubscribe_galerie_imgur', name='unsubscribegalerie'),
    url(r'^(?P<slug>[\-\d\w]+)/sync/$', 'sync_galerie', name='syncgalerie'),
    url(r'^(?P<slug>[\-\d\w]+)/json/$', 'get_json_galerie', name='getjsongalerie'),
    url(r'^(?P<slug>[\-\d\w]+)/$', 'view_galerie', name='viewgalerie'),
)
