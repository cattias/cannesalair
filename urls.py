from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from djblets.util.misc import generate_cache_serials
from django.conf import settings
import os
from admin.forms import GeneralSettingsForm

# Generate cache serials
generate_cache_serials()

if not admin.site._registry:
    admin.autodiscover()

cal_path = os.path.dirname(__file__)
urlpatterns = patterns('',
    (r'^robots\.txt$', 'django.views.static.serve', {'path':'robots.txt', 'document_root': cal_path, 'show_indexes': True}),
    (r'^bc38928ca88b5eaeb8eac84640c15074\.txt$', 'django.views.static.serve', {'path':'bc38928ca88b5eaeb8eac84640c15074.txt', 'document_root': cal_path, 'show_indexes': True}),
    url(r'^search/$', 'django.views.generic.simple.direct_to_template', {'template':'search.html', 'extra_context':{'full':True}}, name="search"),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^article/', include('article.urls')),
    (r'^lien/', include('article.lien_urls')),
    (r'^account/', include('account.urls')),
    (r'^forum/', include('forum.urls')),
    (r'^galerie/', include('galerie.urls')),
    (r'^photologue/', include('photologue.urls')),
    (r'^sortie/', include('sortie.urls')),
    (r'^comment/', include('comment.urls')),
    (r'^captcha/', include('captcha.urls')),
    (r'^core/', include('core.urls')),
    (r'^matos/', include('matos.urls')),
    (r'^meteo/', include('meteo.urls')),
#    (r'^browse/(.*)', login_required(databrowse.site.root)),
)

# And the rest ...
urlpatterns += patterns('',
    url(r'^$', 'article.views.accueil', name="root"),
    url(r'^about/$', 'article.views.about', name="aboutus"),
    url(r'^contactus/$', 'account.forms.contact_us', name="contactus"),
    (r'^secure/(?P<path>.*)$', 'core.views.serve', {
        'show_indexes': True,
        'document_root': settings.SECURE_ROOT,
        }),
)

# Adding the site settings page
urlpatterns += patterns('',
    url(r'admin/settings/general/$', 'djblets.siteconfig.views.site_settings',
     {'form_class': GeneralSettingsForm}, name="site_setup"))

# Add static media
import djblets
import django.contrib.admin
djblets_media_path = os.path.join(os.path.dirname(djblets.__file__), 'media')
admin_media_path = os.path.join(os.path.dirname(django.contrib.admin.__file__), 'media')
urlpatterns += patterns('django.views.static',
    (r'^media/admin/(?P<path>.*)$', 'serve', {
        'show_indexes': True,
        'document_root': admin_media_path,
        }),
    (r'^media/djblets/(?P<path>.*)$', 'serve', {
        'show_indexes': True,
        'document_root': djblets_media_path,
        }),
    (r'^media/(?P<path>.*)$', 'serve', {
        'show_indexes': True,
        'document_root': settings.MEDIA_ROOT,
        }),
)
