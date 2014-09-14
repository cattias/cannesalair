from django.conf import settings
from django.conf.urls.defaults import patterns, url
from photologue.models import Gallery

# Number of random images from the gallery to display.
SAMPLE_SIZE = ":%s" % getattr(settings, 'GALLERY_SAMPLE_SIZE', 6)

# galleries
gallery_args = {'date_field': 'date_added', 'allow_empty': True, 'queryset': Gallery.objects.filter(is_public=True), 'extra_context':{'sample_size':SAMPLE_SIZE}}

urlpatterns = patterns('',
    url(r'^$', 'photologue.views.list_galleries', name="galleries"),
    url(r'^gallery/(?P<slug>[\-\d\w]+)/$', 'photologue.views.view_gallery', name='viewgallery'),
    url(r'^photo/(?P<slug>[\-\d\w]+)/$', 'photologue.views.view_photo', name='viewphoto'),
)
