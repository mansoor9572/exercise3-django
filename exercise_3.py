"""
Exercise 3 & 4 – Demonstration Script

This script demonstrates the Strategy Pattern by calling the
implemented REST API endpoints (Django REST Framework views)
instead of invoking the service layer directly.

Endpoints used:
  POST /songs/generate/     → generate a song via the configured strategy
  GET  /songs/check-status/ → poll the generation task status
  GET  /songs/              → list all songs in the database

Prerequisites:
  1. The Django server must be running:  python manage.py runserver
  2. The .env file must have GENERATOR_STRATEGY set to 'mock' or 'suno'
  3. At least one User must exist (create via Django Admin or createsuperuser)
"""

import sys
import time
import requests

# Fix Windows console encoding for Unicode output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_URL = "http://127.0.0.1:8000"


def get_first_user_id():
    """
    Retrieve the first user_id from the database.
    This is a bootstrap step — in production the user_id
    would come from an authenticated session.
    We use the Django ORM only for this one-time lookup.
    """
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sithara.settings')
    django.setup()

    from music.models import User
    user = User.objects.first()
    if not user:
        from uuid import uuid4
        user = User.objects.create(user_id=uuid4(), email="demo@example.com")
        print(f"    (created demo user: {user.user_id})")
    return str(user.user_id)


def run_demo(mode: str):
    print("=" * 60)
    print(f"[MUSIC] RUNNING DEMONSTRATION IN '{mode.upper()}' MODE")
    print("=" * 60)

    user_id = get_first_user_id()
    print(f"\n[0] Using User ID: {user_id}")

    # ─── Step 1: Generate a song via the REST API ───────────────
    prompt = "A song about getting an A+ in Software Design"
    print(f"\n[1] POST {BASE_URL}/api/songs/generate/")
    print(f"    Payload: prompt='{prompt}', user_id='{user_id}'")

    response = requests.post(
        f"{BASE_URL}/api/songs/generate/",
        json={"prompt": prompt, "user_id": user_id},
    )
    print(f"    HTTP {response.status_code}")
    data = response.json()
    print(f"    Response: {data}")

    if response.status_code != 201:
        print("\n❌ Generation failed. Check server logs.")
        return

    song_id = data.get("song_id")
    task_id = data.get("task_id")   # returned by the generate endpoint

    # ─── Step 2: Check generation status via the REST API ───────
    print(f"\n[2] GET {BASE_URL}/api/songs/check-status/?task_id={task_id}")
    if mode == "suno":
        print("    Waiting 5 seconds for Suno API processing...")
        time.sleep(5)

    status_response = requests.get(
        f"{BASE_URL}/api/songs/check-status/",
        params={"task_id": task_id},
    )
    print(f"    HTTP {status_response.status_code}")
    status_data = status_response.json()
    print(f"    Response: {status_data}")

    # ─── Step 3: List all songs via the REST API ────────────────
    print(f"\n[3] GET {BASE_URL}/api/songs/")
    list_response = requests.get(f"{BASE_URL}/api/songs/")
    print(f"    HTTP {list_response.status_code}")
    songs = list_response.json()
    print(f"    Total songs in DB: {len(songs)}")
    if songs:
        latest = songs[-1]
        print(f"    Latest song:")
        print(f"      - song_id: {latest.get('song_id')}")
        print(f"      - status:  {latest.get('status')}")
        lyrics = latest.get("lyrics") or ""
        print(f"      - lyrics:  {lyrics[:60]}..." if len(lyrics) > 60 else f"      - lyrics:  {lyrics}")

    print("\n" + "-" * 60)
    print("✅ Demonstration complete – all calls made via REST API endpoints.")
    print("-" * 60 + "\n")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "mock"
    print(f"\n📌 Strategy mode: {mode}")
    print(f"📌 Make sure the Django server is running: python manage.py runserver")
    print(f"📌 Make sure .env has GENERATOR_STRATEGY={mode}\n")
    run_demo(mode)
