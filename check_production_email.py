"""
Standalone Production Email Diagnostic Script for UniqueTechCamp.
Run this directly in cPanel / server terminal:
    python check_production_email.py
or with options:
    python check_production_email.py --send-test=your_email@domain.com
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniquetechcamp.settings')
    try:
        import django
        django.setup()
        from django.core.management import call_command
        args = sys.argv[1:]
        call_command('check_production_email', *args)
    except Exception as e:
        print(f"[CRITICAL ERROR] Failed to boot Django environment: {e}")
        import traceback
        traceback.print_exc()
