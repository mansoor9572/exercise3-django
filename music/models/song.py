from django.db import models
from .user import User
from .song_status import SongStatus

class Song(models.Model):
    song_id = models.UUIDField(primary_key=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="songs"
    )

    status = models.CharField(
        max_length=20,
        choices=SongStatus.choices
    )

    lyrics = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.song_id)

    class Meta:
        app_label = 'music'
