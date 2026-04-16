from django.db import models
from .user import User
from .song import Song
from .generation_status import GenerationStatus

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
    external_task_id = models.CharField(max_length=255, null=True, blank=True)

    song = models.OneToOneField(
        Song,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generation_task"
    )

    def __str__(self):
        return str(self.task_id)

    class Meta:
        app_label = 'music'
