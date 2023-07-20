from django.db import models
from base.models import BaseModel
from user.models import User


class TypeNotification(models.TextChoices):
    TIME_TRACKING_HISTORY = "TIME_TRACKING_HISTORY", "TIME_TRACKING_HISTORY"
    WORK_FLOW = "WORK_FLOW", "WORK_FLOW"


class Notification(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    object_id = models.UUIDField(null=False)
    type = models.CharField(
        max_length=128, choices=TypeNotification.choices, null=False)
    checked = models.BooleanField(default=False)
