from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Service, ServiceCategory, ServiceFeature, ServiceFAQ

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(ModelAdmin):
    list_display = ('name', 'icon', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class ServiceFeatureInline(TabularInline):
    model = ServiceFeature
    extra = 1

class ServiceFAQInline(TabularInline):
    model = ServiceFAQ
    extra = 1

@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ('title', 'category', 'icon_name', 'order', 'is_featured', 'is_active')
    list_filter = ('is_active', 'is_featured', 'category')
    search_fields = ('title', 'short_description', 'category__name')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order', 'is_featured', 'is_active')
    inlines = [ServiceFeatureInline, ServiceFAQInline]
