from base.models import BaseModel
from django.db import models
from .time_tracking import TimeTracking


class History(BaseModel):
    time_tracking = models.ForeignKey(
        TimeTracking, on_delete=models.CASCADE, null=False)
    change_detection = models.JSONField(null=False)

