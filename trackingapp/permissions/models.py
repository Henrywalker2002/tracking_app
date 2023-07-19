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
    
    def __str__(self):
        return self.friendly_name
    