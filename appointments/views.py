import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.utils import timezone
from services.models import Service, ServiceCategory
from .models import Appointment
from .emails import send_appointment_emails, generate_ics_content

class AppointmentBookView(View):
    """
    Ultra-Modern Appointment Booking View.
    Supports auto-populating service via '?service=<slug>' query parameter.
    """
    def get(self, request):
        service_slug = request.GET.get('service', '').strip()
        selected_service = None
        if service_slug:
            selected_service = Service.objects.filter(slug=service_slug, is_active=True).first()

        services = Service.objects.filter(is_active=True).select_related('category').order_by('category__order', 'title')
        categories = ServiceCategory.objects.filter(is_active=True).prefetch_related('services')

        # Earliest date is tomorrow (or today if morning)
        min_date = (timezone.now().date() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        max_date = (timezone.now().date() + datetime.timedelta(days=90)).strftime('%Y-%m-%d')

        context = {
            'selected_service': selected_service,
            'services': services,
            'categories': categories,
            'time_slots': Appointment.TIME_SLOT_CHOICES,
            'meeting_types': Appointment.MEETING_TYPE_CHOICES,
            'min_date': min_date,
            'max_date': max_date,
        }
        return render(request, 'appointments/book.html', context)

    def post(self, request):
        service_id = request.POST.get('service_id', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        company_name = request.POST.get('company_name', '').strip()
        preferred_date_str = request.POST.get('preferred_date', '').strip()
        preferred_time_slot = request.POST.get('preferred_time_slot', '').strip()
        meeting_type = request.POST.get('meeting_type', 'google_meet').strip()
        project_description = request.POST.get('project_description', '').strip()

        # Basic validations
        if not (full_name and email and phone and preferred_date_str and preferred_time_slot and project_description):
            messages.error(request, "Please fill in all required fields to schedule your consultation.")
            return redirect(request.get_full_path())

        try:
            preferred_date = datetime.date.fromisoformat(preferred_date_str)
            if preferred_date < timezone.now().date():
                messages.error(request, "Please select an upcoming date for your consultation.")
                return redirect(request.get_full_path())
        except ValueError:
            messages.error(request, "Invalid date format provided. Please pick a valid calendar date.")
            return redirect(request.get_full_path())

        service = None
        if service_id:
            try:
                service = Service.objects.filter(id=service_id, is_active=True).first()
            except Exception:
                pass

        # Create Appointment Record
        appointment = Appointment.objects.create(
            service=service,
            full_name=full_name,
            email=email,
            phone=phone,
            company_name=company_name,
            preferred_date=preferred_date,
            preferred_time_slot=preferred_time_slot,
            meeting_type=meeting_type,
            project_description=project_description,
            status='pending',
        )

        # Dispatch robust notifications (client confirmation + admin alert)
        send_appointment_emails(appointment, request)

        messages.success(request, f"Your consultation has been booked! Reference: {appointment.booking_reference}")
        return redirect('appointments:success', reference=appointment.booking_reference)


class AppointmentSuccessView(View):
    """
    Confirmation landing page displaying appointment summary, calendar sync, and direct contacts.
    """
    def get(self, request, reference):
        appointment = get_object_or_404(Appointment, booking_reference=reference)
        context = {
            'appointment': appointment,
            'whatsapp_url': f"https://wa.me/254715479955?text=Hello%20UniqueTechCamp!%20I%20have%20scheduled%20consultation%20{appointment.booking_reference}%20for%20{appointment.service_name}.",
        }
        return render(request, 'appointments/success.html', context)


class DownloadIcsView(View):
    """
    Endpoint providing direct download of the .ics iCalendar file for Google/Apple/Outlook Calendar.
    """
    def get(self, request, reference):
        appointment = get_object_or_404(Appointment, booking_reference=reference)
        ics_content = generate_ics_content(appointment)

        response = HttpResponse(ics_content, content_type='text/calendar; charset=UTF-8')
        response['Content-Disposition'] = f'attachment; filename="UniqueTechCamp-Consultation-{appointment.booking_reference}.ics"'
        return response
