import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .emails import send_welcome_email

logger = logging.getLogger(__name__)
User = get_user_model()

@receiver(post_save, sender=User)
def dispatch_welcome_email_on_user_creation(sender, instance, created, **kwargs):
    """
    Automatically sends a welcome email when a new user account is created with an email address.
    """
    if created and instance.email:
        try:
            send_welcome_email(
                recipient_email=instance.email,
                user_name=instance.get_full_name() or instance.username,
                user=instance
            )
            logger.info(f"Automated welcome email dispatched to newly registered user: {instance.email}")
        except Exception as e:
            logger.warning(f"Could not dispatch automated welcome email to {instance.email}: {e}")


def clear_site_stats_cache(sender, **kwargs):
    try:
        from django.core.cache import cache
        cache.delete('site_global_stats')
    except Exception:
        pass


try:
    from django.db.models.signals import post_delete
    from services.models import Service, ServiceCategory
    from portfolio.models import Project, ProjectCategory
    from blog.models import Post

    for model in [Service, ServiceCategory, Project, ProjectCategory, Post]:
        post_save.connect(clear_site_stats_cache, sender=model)
        post_delete.connect(clear_site_stats_cache, sender=model)
except Exception:
    pass
