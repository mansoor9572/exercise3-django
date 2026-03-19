from django.db import models

class SongStatus(models.TextChoices):
    READY = "READY", "Ready"
    PROCESSING = "PROCESSING", "Processing"
    FAILED = "FAILED", "Failed"
