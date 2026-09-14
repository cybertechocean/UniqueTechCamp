from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from services.models import Service, ServiceCategory
from blog.models import Post
from portfolio.models import Project

class StaticViewSitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        return [
            'core:home',
            'services:list',
            'blog:list',
            'portfolio:list',
            'core:about',
            'core:contact',
            'core:payment_policy',
            'core:privacy_policy',
            'core:terms_of_service',
            'core:cookie_policy',
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        if item == 'core:home':
            return 1.0
        elif item in ['services:list', 'blog:list']:
            return 0.95
        elif item in ['core:contact', 'core:payment_policy']:
            return 0.9
        return 0.8

class ServiceSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Service.objects.filter(is_active=True).order_by('order', 'title')

    def location(self, item):
        return reverse('services:detail', kwargs={'slug': item.slug})

class ServiceCategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.85

    def items(self):
        return ServiceCategory.objects.filter(is_active=True).order_by('order')

    def location(self, item):
        return f"{reverse('services:list')}?category={item.slug}"

class BlogSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.85

    def items(self):
        return Post.objects.filter(is_published=True).order_by('-published_at')

    def lastmod(self, item):
        return item.updated_at

    def location(self, item):
        return item.get_absolute_url()

class PortfolioSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.75

    def items(self):
        return Project.objects.all().order_by('-created_at')

    def location(self, item):
        return reverse('portfolio:detail', kwargs={'slug': item.slug})
