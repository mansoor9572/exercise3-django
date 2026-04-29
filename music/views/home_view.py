from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from ..models import Song


@method_decorator(ensure_csrf_cookie, name='dispatch')
class HomeView(View):
    """Homepage displaying recent songs."""

    def get(self, request):
        recent_songs = Song.objects.select_related('metadata').order_by('-song_id')[:6]
        return render(request, 'home.html', {
            'active_page': 'home',
            'recent_songs': recent_songs,
        })
