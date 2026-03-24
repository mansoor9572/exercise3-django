from django.http import JsonResponse
from .models import Song

def get_songs(request):
    songs = list(Song.objects.values())
    return JsonResponse(songs, safe=False)

def home(request):
    return JsonResponse({"message": "API is running"})