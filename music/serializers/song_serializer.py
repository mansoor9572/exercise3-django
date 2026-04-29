from rest_framework import serializers
from ..models import Song, AudioFile, SongMetadata


class SongSerializer(serializers.ModelSerializer):
    audio_url = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    mood = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = '__all__'

    def get_audio_url(self, obj):
        try:
            return obj.audio_file.file_url
        except AudioFile.DoesNotExist:
            return None

    def get_title(self, obj):
        try:
            return obj.metadata.title
        except SongMetadata.DoesNotExist:
            return None

    def get_genre(self, obj):
        try:
            return obj.metadata.genre
        except SongMetadata.DoesNotExist:
            return None

    def get_mood(self, obj):
        try:
            return obj.metadata.mood
        except SongMetadata.DoesNotExist:
            return None
