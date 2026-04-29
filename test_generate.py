import os, sys, traceback
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
os.environ['DJANGO_SETTINGS_MODULE'] = 'sithara.settings'

import django
django.setup()

import logging
logging.basicConfig(level=logging.DEBUG)

from music.services.song_service import SongService
from music.models import AudioFile, GenerationTask

print("=" * 50)
print("Testing song generation via Suno API...")
print("=" * 50)

from music.models import User as MusicUser
first_user = MusicUser.objects.first()
print(f"Using user: {first_user.user_id}")

try:
    song = SongService.generate_song_from_prompt(
        str(first_user.user_id), 
        'A happy lo-fi song about summer',
        title='Test Song', genre='Lo-Fi', mood='Calm'
    )
    print(f"\nSong ID: {song.song_id}")
    print(f"Status:  {song.status}")
    print(f"Lyrics:  {(song.lyrics or 'None')[:200]}")
    
    af = AudioFile.objects.filter(song=song).first()
    print(f"Audio:   {af.file_url if af else 'None'}")
    
    task = GenerationTask.objects.filter(song=song).first()
    print(f"Task ID: {task.task_id if task else 'None'}")
    print(f"Task External ID: {task.external_task_id if task else 'None'}")
    print(f"Task Status: {task.status if task else 'None'}")
    
    if song.status != 'READY' and task and task.external_task_id:
        print(f"\nSong not ready yet, polling status...")
        import time
        time.sleep(15)
        result = SongService.check_generation_status(str(task.task_id))
        print(f"Poll result: {result}")
        
        # Refresh song
        song.refresh_from_db()
        print(f"Song status after poll: {song.status}")
        af = AudioFile.objects.filter(song=song).first()
        print(f"Audio after poll: {af.file_url if af else 'None'}")

except Exception as e:
    print(f"\nERROR: {e}")
    traceback.print_exc()
