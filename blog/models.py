from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

class BlogCategory(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, max_length=255)
    category = models.ForeignKey(BlogCategory, related_name='posts', on_delete=models.CASCADE)
    author_name = models.CharField(max_length=100, default="UniqueTechCamp Editorial")
    author_role = models.CharField(max_length=100, default="Lead Systems Architect")
    excerpt = models.TextField(max_length=400, help_text="Short summary for search snippets and preview cards")
    content = CKEditor5Field('Content', config_name='extends')
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    read_time = models.CharField(max_length=30, default="5 min read")
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated keywords (e.g. AI Systems, Lead Generation, WhatsApp)")
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def get_tags_list(self):
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(',') if t.strip()]
