from django.db import models
from .song import Song
from .voice_type import VoiceType

class SongMetadata(models.Model):
    song = models.OneToOneField(
        Song,
        on_delete=models.CASCADE,
        related_name="metadata"
    )

    title = models.CharField(max_length=255)
    occasion = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    mood = models.CharField(max_length=100)

    voice_type = models.CharField(
        max_length=10,
        choices=VoiceType.choices
    )

    description = models.TextField(blank=True)
    date_created = models.DateTimeField()

    class Meta:
        app_label = 'music'
