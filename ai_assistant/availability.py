import datetime
from django.utils import timezone
from appointments.models import Appointment

def get_available_slots_for_date(date_obj: datetime.date) -> dict:
    """
    Checks appointment table to determine availability for the given date.
    Returns:
      {
        "date_str": "YYYY-MM-DD",
        "is_operating_day": bool,
        "message": str,
        "slots": [
            {
                "slot_key": "09:00 - 10:00",
                "label": "09:00 AM - 10:00 AM (EAT)",
                "is_available": True/False
            }, ...
        ]
      }
    """
    today = timezone.now().date()
    
    if date_obj < today:
        return {
            "date_str": date_obj.strftime("%Y-%m-%d"),
            "is_operating_day": False,
            "message": "The selected date is in the past. Please choose an upcoming business day.",
            "slots": []
        }

    # Sunday check (date_obj.weekday() == 6 is Sunday)
    if date_obj.weekday() == 6:
        return {
            "date_str": date_obj.strftime("%Y-%m-%d"),
            "is_operating_day": False,
            "message": "UniqueTechCamp is closed on Sundays. Our consultation hours are Monday through Saturday, 8:00 AM to 8:00 PM EAT.",
            "slots": []
        }

    # Fetch existing appointments on this date that are pending or confirmed
    booked_slots = set(
        Appointment.objects.filter(
            preferred_date=date_obj,
            status__in=['pending', 'confirmed']
        ).values_list('preferred_time_slot', flat=True)
    )

    slot_results = []
    for slot_key, slot_label in Appointment.TIME_SLOT_CHOICES:
        is_free = slot_key not in booked_slots
        # Simple friendly label formatting
        clean_label = slot_label.replace(' (EAT / UTC+3)', '')
        slot_results.append({
            "slot_key": slot_key,
            "label": clean_label,
            "is_available": is_free
        })

    return {
        "date_str": date_obj.strftime("%Y-%m-%d"),
        "date_display": date_obj.strftime("%A, %B %d, %Y"),
        "is_operating_day": True,
        "message": "Available consultation slots for this date:",
        "slots": slot_results
    }


def find_next_available_dates(count: int = 5) -> list:
    """
    Returns upcoming business dates starting tomorrow with at least one free consultation slot.
    """
    results = []
    current = timezone.now().date() + datetime.timedelta(days=1)
    
    while len(results) < count:
        if current.weekday() != 6:  # Skip Sunday
            slot_info = get_available_slots_for_date(current)
            if any(s['is_available'] for s in slot_info['slots']):
                results.append(slot_info)
        current += datetime.timedelta(days=1)
        
    return results
