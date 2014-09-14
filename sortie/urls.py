from sortie.feeds import LatestSortiesFeed
from django.conf.urls.defaults import patterns, url

feeds = {
    'latest': LatestSortiesFeed,
}

urlpatterns = patterns('',
    url(r'^$', 'sortie.views.list_sorties', name="sorties"),
    url(r'^calendar/$', 'sortie.views.calendar_sorties', name="calendarsorties"),
    url(r'^add/$', 'sortie.forms.add_sortie', name='addsortie'),
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}, name="feedsorties"),
    url(r'^changesp/(?P<spid>\d+)/$', 'sortie.forms.change_specialparticipant', name='changespecialparticipant'),
    url(r'^(?P<slug>[\-\d\w]+)/$', 'sortie.views.view_sortie', name="viewsortie"),
    url(r'^(?P<slug>[\-\d\w]+)/edit/$', 'sortie.forms.edit_sortie', name='editsortie'),
    url(r'^(?P<slug>[\-\d\w]+)/cancel/$', 'sortie.forms.cancel_sortie', name="cancelsortie"),
    url(r'^(?P<slug>[\-\d\w]+)/uncancel/$', 'sortie.forms.uncancel_sortie', name="uncancelsortie"),
    url(r'^(?P<slug>[\-\d\w]+)/editcr/$', 'sortie.forms.edit_sortie_cr', name='editsortiecr'),
    url(r'^(?P<slug>[\-\d\w]+)/delete/$', 'sortie.forms.delete_sortie', name='deletesortie'),
    url(r'^(?P<slug>[\-\d\w]+)/participer/$', 'sortie.forms.participer_sortie', name='participersortie'),
    url(r'^(?P<slug>[\-\d\w]+)/annulerparticipation/$', 'sortie.forms.annulerparticiper_sortie', name='annulerparticipersortie'),
    url(r'^(?P<slug>[\-\d\w]+)/participerpeutetre/$', 'sortie.forms.participerpeutetre_sortie', name='participerpeutetresortie'),
    url(r'^(?P<slug>[\-\d\w]+)/subscribe/$', 'sortie.forms.subscribe_sortie_slug', name='subscribesortie'),
    url(r'^(?P<slug>[\-\d\w]+)/unsubscribe/$', 'sortie.forms.unsubscribe_sortie_slug', name='unsubscribesortie'),
)