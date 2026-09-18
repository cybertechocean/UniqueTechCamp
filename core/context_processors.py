import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

def site_stats(request):
    """
    Exposes dynamic counts from the database across all templates:
    - total_services_count (e.g. 165)
    - total_categories_count (e.g. 20)
    - total_projects_count (e.g. 6)
    - total_project_categories_count (e.g. 6)
    - total_blog_posts_count (e.g. 5)

    Cached for 1 hour; automatically falls back if cache table is not yet created.
    """
    stats = None
    try:
        stats = cache.get('site_global_stats')
    except Exception as e:
        logger.debug(f"Cache lookup failed: {e}")

    if stats is None:
        try:
            from services.models import Service, ServiceCategory
            from portfolio.models import Project, ProjectCategory
            from blog.models import Post

            total_services = Service.objects.filter(is_active=True).count()
            total_categories = ServiceCategory.objects.filter(is_active=True).count()
            total_projects = Project.objects.count()
            total_project_cats = ProjectCategory.objects.count()
            total_blog_posts = Post.objects.filter(is_published=True).count()

            stats = {
                'total_services_count': total_services or 165,
                'total_categories_count': total_categories or 20,
                'total_projects_count': total_projects or 6,
                'total_project_categories_count': total_project_cats or 6,
                'total_blog_posts_count': total_blog_posts or 5,
            }
            try:
                cache.set('site_global_stats', stats, 3600)
            except Exception:
                pass
        except Exception as e:
            logger.warning(f"Could not calculate dynamic site stats: {e}")
            stats = {
                'total_services_count': 165,
                'total_categories_count': 20,
                'total_projects_count': 6,
                'total_project_categories_count': 6,
                'total_blog_posts_count': 5,
            }
    return stats
