from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from core.sitemaps import (
    StaticViewSitemap,
    ServiceSitemap,
    ServiceCategorySitemap,
    BlogSitemap,
    PortfolioSitemap,
)
from core.feeds import (
    LatestPostsFeed,
    LatestPostsAtomFeed,
    ServicesFeed,
)
from django.contrib.auth import views as auth_views
from core.views import (
    RobotsTxtView,
    LLMsTxtView,
    EmailPreviewWelcomeView,
    EmailPreviewPasswordResetView,
)

sitemaps = {
    'static': StaticViewSitemap,
    'services': ServiceSitemap,
    'categories': ServiceCategorySitemap,
    'blog': BlogSitemap,
    'portfolio': PortfolioSitemap,
}

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # SEO, Sitemaps & Feeds
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('feed/rss/', LatestPostsFeed(), name='latest_posts_rss'),
    path('feed/atom/', LatestPostsAtomFeed(), name='latest_posts_atom'),
    path('feed/services/', ServicesFeed(), name='services_rss'),
    path('robots.txt', RobotsTxtView.as_view(), name='robots_txt'),
    path('llms.txt', LLMsTxtView.as_view(), name='llms_txt'),
    path('llms-full.txt', LLMsTxtView.as_view(), name='llms_full_txt'),

    # Authentication & Password Reset (Branded with Top Logo & Bottom Social Icons)
    path(
        'auth/password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.txt',
            html_email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
            success_url='/auth/password_reset/done/',
        ),
        name='password_reset'
    ),
    path(
        'auth/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'auth/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url='/auth/reset/done/',
        ),
        name='password_reset_confirm'
    ),
    path(
        'auth/reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # Visual Email In-Browser Previews
    path('emails/preview/welcome/', EmailPreviewWelcomeView.as_view(), name='preview_welcome_email'),
    path('emails/preview/password-reset/', EmailPreviewPasswordResetView.as_view(), name='preview_password_reset_email'),

    # Application routes
    path('', include('core.urls')),
    path('services/', include('services.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('blog/', include('blog.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    from django.views.static import serve
    from django.urls import re_path
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
