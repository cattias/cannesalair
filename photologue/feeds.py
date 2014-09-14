from django.contrib.syndication.feeds import Feed
from photologue.models import Gallery

class LatestGalleriesFeed(Feed):
    title = "CAL site galeries"
    link = "/galleries/"
    description = "Updates on changes and additions to Cannes a l'air galleries."

    def items(self):
        return Gallery.objects.filter(is_public=True).order_by('-date_added')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
