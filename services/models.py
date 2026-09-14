from django.db import models

class ServiceCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=10, default='🔧', help_text="Emoji icon for the category")
    icon_name = models.CharField(max_length=50, blank=True, help_text="Google Material Symbol name (optional)")
    description = models.CharField(max_length=300, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Service Category'
        verbose_name_plural = 'Service Categories'

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(
        ServiceCategory,
        related_name='services',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The industry/service category this service belongs to"
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    icon_name = models.CharField(max_length=50, help_text="Google Material Symbol name")
    short_description = models.CharField(max_length=255)
    overview = models.TextField()
    benefits = models.TextField(help_text="One benefit per line")
    process = models.TextField(help_text="One process step per line")
    featured_image = models.ImageField(upload_to='services/', blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Show this service as featured/highlighted")

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def get_benefits_list(self):
        return [b.strip() for b in self.benefits.split('\n') if b.strip()]

    def get_process_list(self):
        return [p.strip() for p in self.process.split('\n') if p.strip()]

class ServiceFeature(models.Model):
    service = models.ForeignKey(Service, related_name='features', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon_name = models.CharField(max_length=50, help_text="Google Material Symbol name", blank=True)

    def __str__(self):
        return f"{self.service.title} - {self.title}"

class ServiceFAQ(models.Model):
    service = models.ForeignKey(Service, related_name='faqs', on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.service.title} - {self.question}"
