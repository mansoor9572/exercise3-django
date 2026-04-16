import os
import sys
import django
import time

# Fix Windows console encoding for Unicode output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def setup_django(strategy='mock'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sithara.settings')
    os.environ['GENERATOR_STRATEGY'] = strategy
    django.setup()


def run_exercise_3():
    from music.services.song_service import SongService
    from music.models import User, GenerationTask

    # Ensure we have a user
    user = User.objects.first()
    if not user:
        from uuid import uuid4
        user = User.objects.create(user_id=uuid4(), email="test@example.com")

    strategy = os.environ.get('GENERATOR_STRATEGY', 'mock')
    print("=" * 60)
    print(f"[MUSIC] RUNNING DEMONSTRATION IN '{strategy.upper()}' MODE")
    print("=" * 60)

    # 1. Generate Song
    prompt = "A song about getting an A+ in Software Design"
    print(f"\n[1] Initiating Generation Request (prompt: '{prompt}')...")

    song = SongService.generate_song_from_prompt(user.user_id, prompt)
    task = GenerationTask.objects.get(song=song)

    print(f" -> Song DB ID: {song.song_id}")
    print(f" -> GenerationTask DB ID: {task.task_id}")
    print(f" -> External Task ID: {task.external_task_id or 'None yet'}")
    print(f" -> Current Task Status: {task.status}")

    # 2. Check Status
    print("\n[2] Checking Status via API...")
    if strategy == 'suno':
        print(" -> Waiting 5 seconds for Suno API processing...")
        time.sleep(5)

    status_data = SongService.check_generation_status(task.task_id)

    # Reload from DB after checking status
    song.refresh_from_db()
    task.refresh_from_db()

    print(f"\n[Status Data Returned]:")
    print(status_data)

    print(f"\n[3] Final DB State:")
    print(f" -> GenerationTask Status: {task.status}")
    print(f" -> Song Status: {song.status}")
    print(f" -> Lyrics snippet: {song.lyrics[:60]}..." if song.lyrics else " -> Lyrics snippet: None")
    print(f" -> Has Audio File: {'Yes' if hasattr(song, 'audio_file') else 'No'}")
    print("-" * 60 + "\n")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else 'mock'
    setup_django(mode)
    run_exercise_3()
