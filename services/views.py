from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Service, ServiceCategory
import urllib.parse


class ServiceListView(ListView):
    model = Service
    template_name = 'services/list.html'
    context_object_name = 'services'

    def get_queryset(self):
        qs = Service.objects.filter(is_active=True).select_related('category')

        # ── Category filter ──────────────────────────────────────────
        category_slug = self.request.GET.get('category', '').strip()
        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        # ── Search ───────────────────────────────────────────────────
        query = self.request.GET.get('q', '').strip()
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(short_description__icontains=query) |
                Q(overview__icontains=query) |
                Q(category__name__icontains=query)
            )

        # ── Sort ─────────────────────────────────────────────────────
        sort = self.request.GET.get('sort', 'order')
        sort_map = {
            'order':  'order',
            'title':  'title',
            '-title': '-title',
            'newest': '-id',
            'oldest': 'id',
        }
        qs = qs.order_by(sort_map.get(sort, 'order'), 'title')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ServiceCategory.objects.filter(is_active=True)
        context['current_category'] = self.request.GET.get('category', '')
        context['current_q'] = self.request.GET.get('q', '')
        context['current_sort'] = self.request.GET.get('sort', 'order')
        context['total_count'] = self.get_queryset().count()
        return context


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/detail.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.get_object()

        # WhatsApp logic
        current_url = self.request.build_absolute_uri()
        message = (
            f"👋 Hello UniqueTechCamp!\n\n"
            f"I am interested in your *{service.title}* service.\n\n"
            f"Service Link:\n{current_url}\n\n"
            f"Kindly provide me with more information and a quotation.\n\n"
            f"Thank you!"
        )
        encoded_message = urllib.parse.quote(message)
        context['whatsapp_url'] = f"https://wa.me/254715479955?text={encoded_message}"

        context['related_services'] = Service.objects.filter(is_active=True).exclude(id=service.id)[:3]
        return context
