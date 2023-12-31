from base.models import BaseModel
from django.db import models
from user.models import User
from base.models import BaseModel
from datetime import datetime
from trackingapp.custom_middleware import get_current_user
from django.db import transaction
from .release import Release
from django.db import connection, reset_queries
from functools import cached_property


class StatusTimeTracking(models.TextChoices):
    TODO = "TODO", "TODO"
    IN_PROGRESS = "IN_PROGRESS", "IN_PROGRESS"
    IN_REVIEW = "IN_REVIEW", "IN_REVIEW"
    RESOLVED = "RESOLVED", "RESOLVED"
    DEV_TEST = "DEV_TEST", "DEV_TEST"
    QC_TEST = "QC_TEST", "QC_TEST"
    DONE = "DONE", "DONE"


class TimeTracking(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    release = models.ForeignKey(Release, on_delete=models.CASCADE, null=False)
    task_id = models.CharField(null=False, max_length=128, unique= True)
    task_link = models.CharField(max_length=512)
    start_time = models.DateTimeField(null=False, default=datetime.now)
    end_time = models.DateTimeField(null=False)
    status = models.CharField(
        max_length=128, choices=StatusTimeTracking.choices, default=StatusTimeTracking.TODO)
    description = models.TextField(null=True)
    note = models.TextField(null=True)
    is_deleted = models.BooleanField(null=False, default=False)

    def __str__(self):
        return str(self.id)

    @transaction.atomic
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Add default subcriber to who have this task 
        """
        from time_tracking.models.subcriber import Subcriber, SubcriberType
    
        super().save(force_insert, force_update, using, update_fields)
        is_exist = Subcriber.objects.filter(
            user=self.user, time_tracking=self, object_type= SubcriberType.TASK).exists()
        if not is_exist:
            Subcriber.objects.create(user=self.user, time_tracking=self, object_type= SubcriberType.TASK)
