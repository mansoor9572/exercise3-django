import uuid
from django.utils import timezone
from decimal import Decimal
from ..models import Song, AudioFile, GenerationTask, User
from ..models.song_status import SongStatus
from ..models.generation_status import GenerationStatus
from ..strategies import get_generator_strategy, GenerationRequest

class SongService:
    @classmethod
    def generate_song_from_prompt(cls, user_id: str, prompt: str) -> Song:
        """
        Use Case: Generate Song
        Implements the layer coordination between Domain and Infrastructure.
        """
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            user = User.objects.first()
            if not user:
                # create a dummy user if none exist
                user = User.objects.create(user_id=uuid.uuid4(), email="test@example.com")
            
        # 1. Create Song in PROCESSING state
        song = Song.objects.create(
            song_id=uuid.uuid4(),
            user=user,
            status=SongStatus.PROCESSING,
            lyrics=""
        )
        
        # 2. Create GenerationTask (tracking)
        task = GenerationTask.objects.create(
            task_id=uuid.uuid4(),
            user=user,
            status=GenerationStatus.PENDING,
            start_time=timezone.now(),
            song=song
        )
        
        # 3. Call Web Service API via Strategy
        strategy = get_generator_strategy()
        request = GenerationRequest(prompt=prompt)
        result = strategy.generate(request)
        
        # 4. Update Task with external task ID
        task.external_task_id = result.task_id
        task.save()
        
        # Note: In a real system, we'd fire off a Celery task here to poll status.
        # Since Suno API is asynchronous, we won't have lyrics/audio immediately.
        # But MockStrategy returns SUCCESS instantly.
        
        if result.status.upper() == "SUCCESS":
            song.lyrics = result.lyrics or ""
            song.status = SongStatus.READY
            song.save()
            
            task.status = GenerationStatus.COMPLETED
            task.save()
            
            if result.audio_url:
                AudioFile.objects.create(
                    song=song,
                    file_url=result.audio_url,
                    format="MP3",
                    size_in_mb=Decimal("5.00")
                )
        elif result.status.upper() == "FAILED":
            task.status = GenerationStatus.FAILED
            task.save()
            song.status = SongStatus.FAILED
            song.save()
        
        return song

    @classmethod
    def check_generation_status(cls, task_id: str) -> dict:
        task = GenerationTask.objects.get(task_id=task_id)
        
        if task.status in [GenerationStatus.COMPLETED, GenerationStatus.FAILED]:
            return {"status": task.status}
            
        strategy = get_generator_strategy()
        result = strategy.get_status(task.external_task_id or "")
        
        # Update our DB models based on external status
        external_status = result.status.upper()
        
        if external_status == "SUCCESS":
            task.status = GenerationStatus.COMPLETED
            task.save()
            
            song = task.song
            song.lyrics = result.lyrics or ""
            song.status = SongStatus.READY
            song.save()
            
            if result.audio_url:
                AudioFile.objects.get_or_create(
                    song=song,
                    defaults={
                        "file_url": result.audio_url,
                        "format": "MP3",
                        "size_in_mb": Decimal("5.00")
                    }
                )
        elif external_status == "FAILED":
            task.status = GenerationStatus.FAILED
            task.save()
            task.song.status = SongStatus.FAILED
            task.song.save()
            
        return result.raw_response
