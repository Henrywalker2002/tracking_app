from django.db import models
from user.models import User
from base.models import BaseModel
from datetime import datetime

class StatusTimeTracking(models.TextChoices):
    TODO = "TODO" , "TODO"
    IN_PROGRESS = "IN_PROGRESS", "IN_PROGRESS"
    IN_REVIEW = "IN_REVIEW", "IN_REVIEW"
    RESOLVED = "RESOLVED" , "RESOLVED"
    DEV_TEST = "DEV_TEST", "DEV_TEST"
    QC_TEST = "QC_TEST", "QC_TEST"
    DONE =  "DONE","DONE"

class TimeTracking(BaseModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    release = models.CharField(null=False, max_length=128)
    task_id = models.CharField(null=False, max_length=128)
    task_link = models.CharField(max_length=512)
    start_time = models.DateTimeField(null=False, default= datetime.now)
    end_time = models.DateTimeField(null = False)
    status = models.TextField(
        max_length=128, choices=StatusTimeTracking.choices, default=StatusTimeTracking.TODO)

    note = models.TextField()