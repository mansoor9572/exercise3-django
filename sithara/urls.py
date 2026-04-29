from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from music.views import (
    SongViewSet,
    HomeView,
    GenerateView,
    LibraryView,
    SongDetailView,
)

router = DefaultRouter()
router.register(r'songs', SongViewSet, basename='song')

urlpatterns = [
    # Frontend pages (Class-Based Views)
    path('', HomeView.as_view(), name='home'),
    path('generate/', GenerateView.as_view(), name='generate'),
    path('library/', LibraryView.as_view(), name='library'),
    path('song/<uuid:song_id>/', SongDetailView.as_view(), name='song_detail'),

    # Admin
    path('admin/', admin.site.urls),

    # REST API (under /api/ prefix so it doesn't conflict with pages)
    path('api/', include(router.urls)),
]