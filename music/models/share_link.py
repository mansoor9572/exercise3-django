from django.db import models
from .song import Song

class ShareLink(models.Model):
    link_id = models.UUIDField(primary_key=True)

    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name="share_links"
    )

    public_url = models.URLField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.public_url

    class Meta:
        app_label = 'music'
