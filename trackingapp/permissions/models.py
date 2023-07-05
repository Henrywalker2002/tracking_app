from django.db import models
from base.models import BaseModel


class Permission(BaseModel):
    friendly_name = models.CharField( null=False, max_length=128)
    code_name = models.CharField(null=False, max_length=128, unique= True)
    
    def __str__(self):
        return self.friendly_name
    
class Role(BaseModel):
    friendly_name = models.CharField(unique=True, null=False, max_length=128)
    code_name = models.CharField(unique=True, null=False, max_length=128)
    permission = models.ManyToManyField(Permission)

    @property
    def permission_name(self):
        if self.permission:
            return self.permission.all().values_list('friendly_name', flat = True)
        return None 
    
    def __str__(self):
        return self.friendly_name
    
    
