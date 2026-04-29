from django.views import View
from django.shortcuts import render
from ..models import Song


class LibraryView(View):
    """Music library page showing all songs."""

    def get(self, request):
        all_songs = Song.objects.select_related(
            'generation_task', 'metadata'
        ).order_by('-song_id')
        total_count = all_songs.count()
        songs = all_songs[:20]
        return render(request, 'library.html', {
            'active_page': 'library',
            'songs': songs,
            'total_count': total_count,
        })
