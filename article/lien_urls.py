from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'article.views.list_articles', kwargs={'type':'lien'}, name="liens"),
 )