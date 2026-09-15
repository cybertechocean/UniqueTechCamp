from django.db import models
from django.utils import timezone

class ProjectCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Project Categories"

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, related_name='projects')
    client_name = models.CharField(max_length=200, help_text="Client or organization name")
    date = models.DateField(default=timezone.now, help_text="Date when the project was developed / completed")
    technologies = models.CharField(max_length=255, help_text="Comma separated list of technologies")
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    case_study = models.TextField(blank=True)
    results_achieved = models.TextField(help_text="One result per line", blank=True)
    live_demo_url = models.URLField(blank=True, null=True)
    featured_image = models.ImageField(upload_to='portfolio/featured/', blank=True, null=True, help_text="Upload image file from computer")
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Or paste an external image URL (e.g. Unsplash, CDN)")
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-date', '-created_at']

    def __str__(self):
        return self.title

    @property
    def get_image_url(self):
        """Returns uploaded featured image URL if present, otherwise external image URL, or None."""
        if self.featured_image:
            try:
                return self.featured_image.url
            except Exception:
                pass
        if self.image_url:
            return self.image_url
        return None

    def get_technologies_list(self):
        return [t.strip() for t in self.technologies.split(',') if t.strip()]

    def get_results_list(self):
        if not self.results_achieved:
            return []
        return [r.strip() for r in self.results_achieved.split('\n') if r.strip()]

class ProjectScreenshot(models.Model):
    project = models.ForeignKey(Project, related_name='screenshots', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='portfolio/screenshots/', blank=True, null=True, help_text="Upload image file from computer")
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Or paste an external image URL")
    caption = models.CharField(max_length=200, blank=True)

    @property
    def get_image_url(self):
        """Returns uploaded screenshot URL if present, otherwise external image URL, or None."""
        if self.image:
            try:
                return self.image.url
            except Exception:
                pass
        if self.image_url:
            return self.image_url
        return None

    def __str__(self):
        return f"{self.project.title} Screenshot"

