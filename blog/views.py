from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, F
from .models import Post, BlogCategory

class BlogListView(ListView):
    model = Post
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        qs = Post.objects.filter(is_published=True).select_related('category')
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(excerpt__icontains=q) |
                Q(tags__icontains=q) |
                Q(content__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.all()
        category_slug = self.kwargs.get('category_slug')
        context['current_category'] = None
        if category_slug:
            context['current_category'] = get_object_or_404(BlogCategory, slug=category_slug)
        
        context['featured_posts'] = Post.objects.filter(is_published=True, is_featured=True)[:3]
        context['search_query'] = self.request.GET.get('q', '')
        return context

class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        # Safely increment view count
        Post.objects.filter(pk=obj.pk).update(views_count=F('views_count') + 1)
        obj.refresh_from_db()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_posts'] = Post.objects.filter(
            category=self.object.category,
            is_published=True
        ).exclude(pk=self.object.pk)[:3]
        context['categories'] = BlogCategory.objects.all()
        return context
