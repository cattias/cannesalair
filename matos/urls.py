from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'matos.views.list_matos', name="matos"),
    url(r'^(?P<matos_pk>\d+)/$', 'matos.views.view_matos', name="viewmatos"),
)