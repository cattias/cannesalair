from django.contrib.syndication.feeds import Feed
from galerie.models import Galerie

class LatestGaleriesFeed(Feed):
    title = "CAL site galeries"
    link = "/galeries/"
    description = "Updates on changes and additions to Cannes a l'air galleries."

    def items(self):
        return Galerie.objects.all().order_by('-date_publication')[:10]

    def item_title(self, item):
        return item.titre

    def item_description(self, item):
        return item.description
