from django.db import models

class GenerationStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    PROCESSING = "PROCESSING", "Processing"
    RETRYING = "RETRYING", "Retrying"
    COMPLETED = "COMPLETED", "Completed"
    FAILED = "FAILED", "Failed"
    TIMED_OUT = "TIMED_OUT", "TimedOut"
