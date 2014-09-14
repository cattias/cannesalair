from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'meteo.views.list_previ', name="listprevi"),
    url(r'^add/$', 'meteo.forms.add_previ', name='addprevi'),
    url(r'^(?P<previid>\d+)/$', 'meteo.views.view_previ', name="viewprevi"),
    url(r'^(?P<previid>\d+)/edit/$', 'meteo.forms.edit_previ', name='editprevi'),
    url(r'^(?P<previid>\d+)/delete/$', 'meteo.forms.delete_previ', name='deleteprevi'),
    url(r'^encartmeteo/$', 'meteo.views.encartmeteo', name='encartmeteo'),
)