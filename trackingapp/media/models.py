from django.db import models
from base.models import BaseModel


class ContentTypeChoices(models.TextChoices):
    TEXT_PLAIN = "TEXT_PLAIN", "TEXT_PLAIN"
    HTML = "HTML", "HTML"


class SendMethodChoices(models.TextChoices):
    EMAIL = "EMAIL", "EMAIL"
    MESSAGE = "MESSAGE", "MESSAGE"
    SMS = "SMS", "SMS"


class MediaStatusChoices(models.TextChoices):
    IN_QUEUE = "IN_QUEUE", "IN_QUEUE"
    IN_PROCESS = "IN_PROCESS", "IN_PROCESS"
    SUCCESS = "SUCCESS", "SUCCESS"
    FAIL = "FAIL", "FAIL"


class Media(BaseModel):
    media_from = models.JSONField(null=False, db_column = "from")
    media_to = models.JSONField(null=False)
    content = models.TextField(null=False)
    context_type = models.CharField(
        max_length=128, choices=ContentTypeChoices.choices, default=ContentTypeChoices.TEXT_PLAIN, null=False)
    sending_method = models.CharField(
        max_length=128, choices=SendMethodChoices.choices, null=False)
    status = models.CharField(max_length=128, choices=MediaStatusChoices.choices,
                              default=MediaStatusChoices.IN_QUEUE, null=False)
    retry_count = models.IntegerField(default= 0)
