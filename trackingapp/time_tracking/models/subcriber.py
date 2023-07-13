from base.models import BaseModel
from django.core.cache import cache
from django.db import models
from .time_tracking import TimeTracking
from user.models import User
from .release import Release


class SubcriberType(models.TextChoices):
    RELEASE = "RELEASE", "RELEASE"
    TASK = "TASK", "TASK"


class Subcriber(BaseModel):
    time_tracking = models.ForeignKey(
        TimeTracking, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    release = models.ForeignKey(Release, on_delete=models.CASCADE, null=True)
    object_type = models.CharField(
        max_length=128, choices=SubcriberType.choices, null=False)

    @property
    def email_user(self):
        return (cache.get(self.user_id) if cache.get(self.user_id)
                else cache.get_or_set(self.user_id, self.user.email))
