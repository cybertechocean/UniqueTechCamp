#!/usr/bin/env python
"""
UniqueTechCamp AI Assistant & Prompts Production Diagnostic Tool
Usage:
    Internal check (local Django environment):
        python check_ai_endpoints.py
    
    Live remote check (against production domain):
        python check_ai_endpoints.py --remote https://uniquetechcamp.org
"""
import os
import sys
import json
import time

def run_internal_diagnostics():
    print("=" * 70)
    print("UNIQUETECHCAMP AI ASSISTANT: INTERNAL DIAGNOSTIC SUITE")
    print("=" * 70)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniquetechcamp.settings')
    try:
        import django
        django.setup()
        from django.core.management import call_command
        call_command('migrate', verbosity=0)
    except Exception as e:
        print(f"[FAIL] Failed to initialize Django: {e}")
        return False

    from django.test import Client

    client = Client()
    passed = 0
    total = 0

    endpoints_to_test = [
        ('init', '/ai-assistant/api/init/', 'POST', {}),
        ('lead', '/ai-assistant/api/lead/', 'POST', {
            'full_name': 'Production Diagnostic User',
            'email': 'diagnostic@uniquetechcamp.org',
            'phone': '+254715479955'
        }),
        ('capture-lead (alias)', '/ai-assistant/api/capture-lead/', 'POST', {
            'full_name': 'Production Diagnostic User',
            'email': 'diagnostic2@uniquetechcamp.org',
            'phone': '+254715479955'
        }),
        ('message', '/ai-assistant/api/message/', 'POST', {
            'message': 'Who are you and what systems do you build?'
        }),
        ('availability', '/ai-assistant/api/availability/?date=2026-09-22', 'GET', {}),
        ('transcript', '/ai-assistant/api/transcript/', 'POST', {}),
        ('email-transcript (alias)', '/ai-assistant/api/email-transcript/', 'POST', {}),
    ]

    session_id = None

    for name, path, method, payload in endpoints_to_test:
        total += 1
        print(f"\n[Test {total}] Testing {method} {path} ({name})...")
        t0 = time.time()

        if session_id and method == 'POST':
            payload['session_id'] = session_id

        try:
            if method == 'POST':
                res = client.post(path, data=json.dumps(payload), content_type='application/json')
            else:
                res = client.get(path)
            duration_ms = int((time.time() - t0) * 1000)

            if res.status_code == 404:
                print(f"  [FAIL] 404 NOT FOUND - Route {path} is missing from urls.py!")
                continue
            elif res.status_code >= 500:
                print(f"  [FAIL] {res.status_code} SERVER ERROR - ({duration_ms}ms)")
                print(f"     Response body: {res.content[:200]}")
                continue

            try:
                data = res.json()
            except Exception:
                print(f"  [WARN] Non-JSON response ({res.status_code}): {res.content[:150]}")
                continue

            if name == 'init' and data.get('session_id'):
                session_id = data['session_id']
                print(f"  [PASS] HTTP {res.status_code} ({duration_ms}ms) | Initialized Session: {session_id}")
            else:
                print(f"  [PASS] HTTP {res.status_code} ({duration_ms}ms) | success={data.get('success')}")

            passed += 1

        except Exception as err:
            print(f"  [ERROR] {err}")

    print("\n" + "=" * 70)
    print(f"RESULTS: {passed}/{total} endpoints PASSED.")
    print("=" * 70)
    return passed == total


def run_remote_diagnostics(base_url):
    print("=" * 70)
    print(f"UNIQUETECHCAMP AI ASSISTANT: REMOTE CHECK -> {base_url}")
    print("=" * 70)

    try:
        import urllib.request
        import urllib.error
    except ImportError:
        print("Standard urllib not available.")
        return False

    session_id = None
    base_url = base_url.rstrip('/')

    endpoints = [
        ('init', f"{base_url}/ai-assistant/api/init/", 'POST', {}),
        ('lead', f"{base_url}/ai-assistant/api/lead/", 'POST', {
            'full_name': 'Production Verification Test',
            'email': 'verify@uniquetechcamp.org',
            'phone': '+254715479955'
        }),
        ('capture-lead', f"{base_url}/ai-assistant/api/capture-lead/", 'POST', {
            'full_name': 'Production Verification Test',
            'email': 'verify2@uniquetechcamp.org',
            'phone': '+254715479955'
        }),
    ]

    for name, url, method, payload in endpoints:
        print(f"\nProbing {method} {url}...")
        t0 = time.time()
        try:
            req_data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                url,
                data=req_data,
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'UniqueTechCamp-Diagnostic/1.0'
                }
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                status = response.status
                duration_ms = int((time.time() - t0) * 1000)
                body = response.read().decode('utf-8', errors='replace')
                print(f"  [PASS] HTTP {status} ({duration_ms}ms): {body[:150]}")
        except urllib.error.HTTPError as e:
            duration_ms = int((time.time() - t0) * 1000)
            print(f"  [FAIL] HTTP ERROR {e.code} ({duration_ms}ms): {e.reason}")
            try:
                err_body = e.read().decode('utf-8', errors='replace')
                print(f"     Body: {err_body[:200]}")
            except Exception:
                pass
        except Exception as e:
            print(f"  [ERROR] {e}")

    print("\n" + "=" * 70)


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--remote':
        run_remote_diagnostics(sys.argv[2])
    else:
        success = run_internal_diagnostics()
        sys.exit(0 if success else 1)
