from article.feeds import LatestArticlesFeed
from django.conf.urls.defaults import patterns, url

feeds = {
    'latest': LatestArticlesFeed,
}

urlpatterns = patterns('',
    url(r'^$', 'article.views.list_articles', name="articles"),
    url(r'^add/$', 'article.forms.create_new_article', name='addarticle'),
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}, name="feedarticles"),
    url(r'^(?P<slug>[\-\d\w]+)/$', 'article.views.view_article', name="viewarticle"),
    url(r'^(?P<slug>[\-\d\w]+)/edit/$', 'article.forms.edit_article', name='editarticle'),
    url(r'^(?P<slug>[\-\d\w]+)/delete/$', 'article.forms.delete_article', name='deletearticle'),
    url(r'^(?P<slug>[\-\d\w]+)/subscribe/$', 'article.forms.subscribe_article_slug', name='subscribearticle'),
    url(r'^(?P<slug>[\-\d\w]+)/unsubscribe/$', 'article.forms.unsubscribe_article_slug', name='unsubscribearticle'),
 )