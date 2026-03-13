from django.contrib import admin
from .models import (
    User,
    Song,
    GenerationTask,
    ShareLink,
    SongMetadata,
    AudioFile
)

admin.site.register(User)
admin.site.register(Song)
admin.site.register(GenerationTask)
admin.site.register(ShareLink)
admin.site.register(SongMetadata)
admin.site.register(AudioFile)