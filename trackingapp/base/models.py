import uuid
from django.db import models
from user.models import User
from trackingapp.custom_middleware import get_current_user


class BaseModel(models.Model):
    """
    BaseModel contains id, created_at, modified_at, created_by, updated_by, email_created_by, email_updated_by
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_created_by", default= get_current_user, null = True)
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_updated_by", null= True)
    
    @property
    def email_created_by(self):
        if self.created_by:
            return self.created_by.email
        return None 
    
    @property
    def email_updated_by(self):
        if self.updated_by:
            return self.updated_by.email 
        return None

    class Meta: 
        abstract = True
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.updated_by = get_current_user()
        return super().save(force_insert, force_update, using, update_fields)
    
