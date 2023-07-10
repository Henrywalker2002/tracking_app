from base.models import BaseModel
from django.core.cache import cache
from django.db import models
from .time_tracking import TimeTracking


class History(BaseModel):
    time_tracking = models.ForeignKey(
        TimeTracking, on_delete=models.CASCADE, null=False)
    change_detection = models.JSONField(null=False)

    @property
    def email_user(self):
        if cache.get(self.user_id):
            return cache.get(self.user_id)
        elif self.user:
            return cache.get_or_set(self.user_id, self.user.email)

