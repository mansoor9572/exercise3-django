import uuid
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from music.models import (
    User, Song, SongMetadata, AudioFile,
    GenerationTask, ShareLink,
)
from music.models.song_status import SongStatus
from music.models.generation_status import GenerationStatus
from music.models.voice_type import VoiceType
from music.strategies import (
    GenerationRequest, GenerationResult, StrategyFactory,
)
from music.strategies.mock_song_generator_strategy import MockSongGeneratorStrategy


class UserModelTest(TestCase):
    """Tests for the User domain entity."""

    def test_create_user(self):
        user = User.objects.create(user_id=uuid.uuid4(), email="test@example.com")
        self.assertEqual(str(user), "test@example.com")

    def test_email_unique(self):
        User.objects.create(user_id=uuid.uuid4(), email="dup@example.com")
        with self.assertRaises(Exception):
            User.objects.create(user_id=uuid.uuid4(), email="dup@example.com")


class SongModelTest(TestCase):
    """Tests for the Song domain entity."""

    def setUp(self):
        self.user = User.objects.create(user_id=uuid.uuid4(), email="song@test.com")

    def test_create_song(self):
        song = Song.objects.create(
            song_id=uuid.uuid4(), user=self.user,
            status=SongStatus.PROCESSING, lyrics=""
        )
        self.assertEqual(song.status, SongStatus.PROCESSING)
        self.assertEqual(song.user, self.user)

    def test_song_str(self):
        sid = uuid.uuid4()
        song = Song.objects.create(
            song_id=sid, user=self.user,
            status=SongStatus.READY, lyrics="test"
        )
        self.assertEqual(str(song), str(sid))

    def test_song_status_choices(self):
        self.assertIn(("READY", "Ready"), SongStatus.choices)
        self.assertIn(("PROCESSING", "Processing"), SongStatus.choices)
        self.assertIn(("FAILED", "Failed"), SongStatus.choices)


class SongMetadataModelTest(TestCase):
    """Tests for the SongMetadata domain entity."""

    def setUp(self):
        self.user = User.objects.create(user_id=uuid.uuid4(), email="meta@test.com")
        self.song = Song.objects.create(
            song_id=uuid.uuid4(), user=self.user,
            status=SongStatus.READY, lyrics=""
        )

    def test_create_metadata(self):
        meta = SongMetadata.objects.create(
            song=self.song, title="Test Song",
            occasion="Birthday", genre="Pop", mood="Happy",
            voice_type=VoiceType.FEMALE,
            description="A test description",
            date_created=timezone.now()
        )
        self.assertEqual(meta.title, "Test Song")
        self.assertEqual(meta.voice_type, VoiceType.FEMALE)


class GenerationTaskModelTest(TestCase):
    """Tests for the GenerationTask domain entity."""

    def setUp(self):
        self.user = User.objects.create(user_id=uuid.uuid4(), email="task@test.com")
        self.song = Song.objects.create(
            song_id=uuid.uuid4(), user=self.user,
            status=SongStatus.PROCESSING, lyrics=""
        )

    def test_create_task(self):
        task = GenerationTask.objects.create(
            task_id=uuid.uuid4(), user=self.user,
            status=GenerationStatus.PENDING,
            start_time=timezone.now(), song=self.song
        )
        self.assertEqual(task.status, GenerationStatus.PENDING)
        self.assertEqual(task.retry_count, 0)


class MockStrategyTest(TestCase):
    """Tests for the MockSongGeneratorStrategy."""

    def test_generate_returns_success(self):
        strategy = MockSongGeneratorStrategy()
        request = GenerationRequest(prompt="test prompt")
        result = strategy.generate(request)
        self.assertEqual(result.status, "SUCCESS")
        self.assertIsNotNone(result.audio_url)
        self.assertIn("test prompt", result.lyrics)

    def test_get_status_returns_success(self):
        strategy = MockSongGeneratorStrategy()
        result = strategy.get_status("mock-123")
        self.assertEqual(result.status, "SUCCESS")


class StrategyFactoryTest(TestCase):
    """Tests for the StrategyFactory."""

    def test_default_returns_mock(self):
        with self.settings(GENERATOR_STRATEGY='mock'):
            strategy = StrategyFactory.get_generator_strategy()
            self.assertIsInstance(strategy, MockSongGeneratorStrategy)

    def test_unknown_falls_back_to_mock(self):
        with self.settings(GENERATOR_STRATEGY='unknown'):
            strategy = StrategyFactory.get_generator_strategy()
            self.assertIsInstance(strategy, MockSongGeneratorStrategy)
