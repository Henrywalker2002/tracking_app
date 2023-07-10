from base.models import BaseModel
from django.db import models

class WorkflowStatus(models.TextChoices):
    DRAFT = "DRAFT", "DRAFT"
    ACTIVE = "ACTIVE", "ACTIVE"
    IN_ACTIVE = "IN_ACTIVE", "IN_ACTIVE"


class Workflow(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    status = models.CharField(
        max_length=128, choices=WorkflowStatus.choices, default=WorkflowStatus.DRAFT)
    is_default = models.BooleanField(default=None)


class WorkflowStepMeetCondition(models.TextChoices):
    ANY = "ANY", "ANY"
    ALL = "ALL", "ALL"

class WorkflowStep(BaseModel):
    description = models.TextField()
    meet_condition = models.CharField(max_length= 128, choices= WorkflowStepMeetCondition.choices)
    order = models.IntegerField()
    workflow = models.ForeignKey(Workflow, on_delete= models.CASCADE)
    
class Condition(BaseModel):
    field_type = models.CharField(max_length= 128)
    property = models.CharField(max_length= 128)
    operator = models.CharField(max_length= 128)
    values = models.JSONField()
    order = models.IntegerField()
    field_property = models.CharField(max_length= 128)
    workflow_step = models.ForeignKey(WorkflowStep, on_delete= models.CASCADE)