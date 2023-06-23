import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=128)
    password = models.CharField(max_length=128, null=False)
    first_name = models.CharField(max_length=128, null=False)
    last_name = models.CharField(max_length=128, null=False)
    phone = models.CharField(max_length=128, null=False)
    is_active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    roles = models.ManyToManyField(to = "permissions.Role")
    
    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name
    
    USERNAME_FIELD = 'email'
    objects = BaseUserManager()

    def __str__(self):
        return self.email
