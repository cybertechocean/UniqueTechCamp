from django.contrib import admin
from .models import Project, ProjectCategory, ProjectScreenshot

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class ProjectScreenshotInline(admin.TabularInline):
    model = ProjectScreenshot
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'client_name', 'order', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'client_name', 'technologies', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order',)
    inlines = [ProjectScreenshotInline]
