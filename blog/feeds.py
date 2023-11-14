from .models import Entry
from django.contrib.syndication.views import Feed
from django.urls import reverse


class EntriesFeed(Feed):
    title = "Blog Entries"
    description = "Latest entries posted to my blog."

    def link(self):
        return reverse("blog:index")

    def items(self):
        return Entry.objects.published().reverse_chronological()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.created_at

    def item_updateddate(self, item):
        return item.updated_at
