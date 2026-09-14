from django.contrib import admin
from .models import Service, ServiceCategory, ServiceFeature, ServiceFAQ


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1

class ServiceFAQInline(admin.TabularInline):
    model = ServiceFAQ
    extra = 1

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'icon_name', 'order', 'is_featured', 'is_active')
    list_filter = ('is_active', 'is_featured', 'category')
    search_fields = ('title', 'short_description', 'category__name')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order', 'is_featured', 'is_active')
    inlines = [ServiceFeatureInline, ServiceFAQInline]
    autocomplete_fields = []
