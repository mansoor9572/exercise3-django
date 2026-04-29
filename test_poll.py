import os, sys, time, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
os.environ['DJANGO_SETTINGS_MODULE'] = 'sithara.settings'

import django
django.setup()

import logging
logging.basicConfig(level=logging.INFO)

from music.services.song_service import SongService
from music.models import AudioFile, GenerationTask

print("=" * 50)
print("Testing LONG song generation via Suno API...")
print("=" * 50)

try:
    # Use existing task if available or create a new one
    from music.models import User as MusicUser
    first_user = MusicUser.objects.first()
    
    song = SongService.generate_song_from_prompt(
        str(first_user.user_id), 
        'A sad lo-fi song about rain',
        title='Rainy Mood', genre='Lo-Fi', mood='Melancholy'
    )
    
    task = GenerationTask.objects.filter(song=song).first()
    task_id = str(task.task_id)
    
    print(f"Generated song. DB Task ID: {task_id}")
    print("Starting continuous polling...")
    
    attempts = 0
    while attempts < 30:
        attempts += 1
        print(f"\n--- Poll {attempts} ---")
        
        result = SongService.check_generation_status(task_id)
        print(f"Result dict: {result}")
        
        if result.get("status") in ["COMPLETED", "SUCCESS", "FAILED"]:
            print(f"Final status reached: {result.get('status')}")
            break
            
        time.sleep(5)
        
except Exception as e:
    import traceback
    traceback.print_exc()
