from django.db import models


# ENUMERATIONS
class SongStatus(models.TextChoices):
    READY = "READY", "Ready"
    PROCESSING = "PROCESSING", "Processing"
    FAILED = "FAILED", "Failed"


class GenerationStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    PROCESSING = "PROCESSING", "Processing"
    RETRYING = "RETRYING", "Retrying"
    COMPLETED = "COMPLETED", "Completed"
    FAILED = "FAILED", "Failed"
    TIMED_OUT = "TIMED_OUT", "TimedOut"


class VoiceType(models.TextChoices):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"
    OTHER = "OTHER", "Other"


# ENTITY: User
class User(models.Model):
    user_id = models.UUIDField(primary_key=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


# ENTITY: Song
class Song(models.Model):
    song_id = models.UUIDField(primary_key=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="songs"
    )

    status = models.CharField(
        max_length=20,
        choices=SongStatus.choices
    )

    lyrics = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.song_id)


# ENTITY: GenerationTask
class GenerationTask(models.Model):
    task_id = models.UUIDField(primary_key=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="generation_tasks"
    )

    status = models.CharField(
        max_length=20,
        choices=GenerationStatus.choices
    )

    start_time = models.DateTimeField()

    retry_count = models.IntegerField(default=0)

    backgrounded = models.BooleanField(default=False)

    song = models.OneToOneField(
        Song,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generation_task"
    )

    def __str__(self):
        return str(self.task_id)


# ENTITY: ShareLink
class ShareLink(models.Model):
    link_id = models.UUIDField(primary_key=True)

    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name="share_links"
    )

    public_url = models.URLField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.public_url


# VALUE OBJECT: SongMetadata
class SongMetadata(models.Model):
    song = models.OneToOneField(
        Song,
        on_delete=models.CASCADE,
        related_name="metadata"
    )

    title = models.CharField(max_length=255)
    occasion = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    mood = models.CharField(max_length=100)

    voice_type = models.CharField(
        max_length=10,
        choices=VoiceType.choices
    )

    description = models.TextField(blank=True)

    date_created = models.DateTimeField()


# VALUE OBJECT: AudioFile
class AudioFile(models.Model):
    song = models.OneToOneField(
        Song,
        on_delete=models.CASCADE,
        related_name="audio_file"
    )

    file_url = models.URLField()

    format = models.CharField(max_length=10, default="MP3")

    size_in_mb = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )