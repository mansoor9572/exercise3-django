from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from music.views import home, SongViewSet

router = DefaultRouter()
router.register(r'songs', SongViewSet, basename='song')

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]