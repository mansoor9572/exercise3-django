from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Song, GenerationTask
from ..serializers import SongSerializer
from ..services.song_service import SongService


class SongViewSet(viewsets.ModelViewSet):
    """REST API ViewSet for Song CRUD and generation endpoints."""

    queryset = Song.objects.all()
    serializer_class = SongSerializer
    authentication_classes = []   # disable CSRF enforcement for API
    permission_classes = []

    @action(detail=False, methods=['post'], url_path='generate')
    def generate_song(self, request):
        prompt = request.data.get('prompt')
        user_id = request.data.get('user_id')
        title = request.data.get('title', '')
        genre = request.data.get('genre', '')
        mood = request.data.get('mood', '')
        description = request.data.get('description', '')

        # If user_id not provided (from frontend), pick the first user
        if not user_id:
            from ..models import User
            user = User.objects.first()
            if user:
                user_id = str(user.user_id)

        if not prompt or not user_id:
            return Response(
                {"error": "prompt and user_id are required fields"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            song = SongService.generate_song_from_prompt(
                user_id, prompt,
                title=title, genre=genre, mood=mood, description=description
            )
            serializer = self.get_serializer(song)
            # Include the task_id so callers can poll status via the API
            task = GenerationTask.objects.filter(song=song).first()
            response_data = serializer.data
            response_data['task_id'] = str(task.task_id) if task else None
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='check-status')
    def check_status(self, request):
        task_id = request.query_params.get('task_id')
        if not task_id:
            return Response({"error": "task_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            status_data = SongService.check_generation_status(task_id)
            return Response(status_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
