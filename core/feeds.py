from django.contrib.syndication.feeds import Feed
from core.models import AttributeLogEntry
from django.contrib.admin.models import LogEntry
from django.core.urlresolvers import reverse

class LatestLogEntriesFeed(Feed):
    title = "Cannes A L'air"
    link = "/"
    description = "Toutes les modifications du site."

    def items(self):
        return LogEntry.objects.order_by('-action_time')[:10]

    def item_title(self, item):
        return item.action_flag + " - " + item.content_type

    def item_link(self, item):
        return reverse("root")

class LatestAttributeLogEntriesFeed(Feed):
    title = "Cannes A L'air"
    link = "/"
    description = "Toutes les modifications du site."

    def items(self):
        return AttributeLogEntry.objects.order_by('-action_time')[:10]

    def item_title(self, item):
        return item.action_flag + " - " + item.content_type

    def item_link(self, item):
        return reverse("root")
