from django.contrib.syndication.feeds import Feed
from article.models import Article

class LatestArticlesFeed(Feed):
    title = "CAL site articles"
    link = "/articles/"
    description = "Updates on changes and additions to Cannes a l'air articles."

    def items(self):
        return Article.objects.order_by('-date_publication')[:10]

    def item_title(self, item):
        return item.titre

    def item_description(self, item):
        return item.contenu
