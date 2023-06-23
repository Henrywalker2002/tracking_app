import uuid
from django.db import models
from user.models import User
from trackingapp.custom_middleware import get_current_user

# Create your models here.
class BaseModel(models.Model):
    """
    BaseModel contains id, created_at, modified_at, created_by, updated_by 
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_created_by", default= get_current_user)
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_updated_by", null= True)

    
    class Meta: 
        abstract = True
    