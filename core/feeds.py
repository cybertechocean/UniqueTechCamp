from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.urls import reverse
from blog.models import Post
from services.models import Service

class LatestPostsFeed(Feed):
    title = "UniqueTechCamp - AI Systems, Web Architecture & Digital Growth"
    link = "/blog/"
    description = "Actionable insights on AI Lead Generation, 24/7 WhatsApp Qualification Bots, and Modern Web Systems by UniqueTechCamp (Nairobi, Kenya)."
    language = "en-gb"

    def items(self):
        return Post.objects.filter(is_published=True).order_by('-published_at')[:25]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.published_at

    def item_author_name(self, item):
        return item.author_name

    def item_categories(self, item):
        return [item.category.name] + item.get_tags_list()

class LatestPostsAtomFeed(LatestPostsFeed):
    feed_type = Atom1Feed
    subtitle = LatestPostsFeed.description

class ServicesFeed(Feed):
    title = "UniqueTechCamp - Complete Service Catalogue & AI Growth Systems"
    link = "/services/"
    description = "100+ specialized industry web development systems integrated with AI Lead Generation, WhatsApp/Email Lead Qualification, and automated follow-ups."
    language = "en-gb"

    def items(self):
        return Service.objects.filter(is_active=True).order_by('order', 'title')[:50]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.short_description

    def item_link(self, item):
        return reverse('services:detail', kwargs={'slug': item.slug})

    def item_categories(self, item):
        return [item.category.name] if item.category else []
