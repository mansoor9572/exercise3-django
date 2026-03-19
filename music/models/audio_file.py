from django.db import models
from .song import Song

class AudioFile(models.Model):
    song = models.OneToOneField(
        Song,
        on_delete=models.CASCADE,
        related_name="audio_file"
    )

    file_url = models.URLField()
    format = models.CharField(max_length=10, default="MP3")

    size_in_mb = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    class Meta:
        app_label = 'music'
