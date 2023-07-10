from base.models import BaseModel
from django.db import models
from datetime import datetime


class ReleaseStatus(models.TextChoices):
    TODO = "TODO", "TODO"
    IN_PROGRESS = "IN_PROGRESS", "IN_PROGRESS"
    DONE = "DONE", "DONE"


class Release(BaseModel):
    release = models.CharField(max_length=128, null=False)
    start_time = models.DateTimeField(null=False, default=datetime.now)
    end_time = models.DateTimeField(null=False)
    status = models.CharField(
        max_length=128, choices=ReleaseStatus.choices, null=False, default=ReleaseStatus.TODO)
    description = models.TextField()
    is_deleted = models.BooleanField(default=False, null=False)
