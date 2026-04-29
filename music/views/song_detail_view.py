from django.views import View
from django.shortcuts import render, get_object_or_404
from ..models import Song, AudioFile, SongMetadata


class SongDetailView(View):
    """Detail page for a single song."""

    def get(self, request, song_id):
        song = get_object_or_404(Song, song_id=song_id)
        audio = AudioFile.objects.filter(song=song).first()
        metadata = SongMetadata.objects.filter(song=song).first()
        return render(request, 'song_detail.html', {
            'active_page': 'library',
            'song': song,
            'audio': audio,
            'metadata': metadata,
        })
