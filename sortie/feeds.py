from django.contrib.syndication.feeds import Feed
from sortie.models import Sortie

class LatestSortiesFeed(Feed):
    title = "CAL site activites"
    link = "/sorties/"
    description = "Updates on changes and additions to Cannes a l'air activites."

    def items(self):
        return Sortie.objects.order_by('-date_debut')[:10]

    def item_title(self, item):
        return item.titre

    def item_description(self, item):
        return item.description
